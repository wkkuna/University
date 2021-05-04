#include <readline/readline.h>
#include <readline/history.h>

#define DEBUG 0

#include "shell.h"

sigset_t sigchld_mask;

static sigjmp_buf loop_env;

static void sigint_handler(int sig) {
  siglongjmp(loop_env, sig);
}

/* Rewrite closed file descriptors to -1,
 * to make sure we don't attempt do close them twice. */
static void MaybeClose(int *fdp) {
  if (*fdp < 0)
    return;
  Close(*fdp);
  *fdp = -1;
}

/* Consume all tokens related to redirection operators.
 * Put opened file descriptors into inputp & output respectively. */
static int do_redir(token_t *token, int ntokens, int *inputp, int *outputp) {
  token_t mode = NULL; /* T_INPUT, T_OUTPUT or NULL */
  int n = 0;           /* number of tokens after redirections are removed */

  /* rw-rw-rw */
  int permissions = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH;

  for (int i = 0; i < ntokens; i++) {
    /* TODO: Handle tokens and open files as requested. */

    mode = token[i];
    token_t IO = token[i + 1];

    if (mode == T_INPUT) {
      /* Possibly input from pipeline */
      MaybeClose(inputp);

      /* Open to read only */
      *inputp = Open(IO, O_RDONLY, 0);
      n += 2;
    }

    else if (mode == T_OUTPUT) {
      /* Possibly output from pipeline */
      MaybeClose(outputp);

      /* If non-existent create with permissions, open to write only */
      *outputp = Open(IO, O_WRONLY | O_CREAT, permissions);
      n += 2;
    }
  }

  n = ntokens - n;
  token[n] = NULL;
  return n;
}

/* Execute internal command within shell's process or execute external command
 * in a subprocess. External command can be run in the background. */
static int do_job(token_t *token, int ntokens, bool bg) {
  int input = -1, output = -1;
  int exitcode = 0;

  ntokens = do_redir(token, ntokens, &input, &output);

  if (!bg) {
    if ((exitcode = builtin_command(token)) >= 0)
      return exitcode;
  }

  sigset_t mask;
  Sigprocmask(SIG_BLOCK, &sigchld_mask, &mask);

  /* TODO: Start a subprocess, create a job and monitor it. */
  pid_t pid = Fork();

  /* Set child group both in parent and child
   since parent doesn't always have
   permission to change child's group */
  Setpgid(pid, pid);

  /* Child */
  if (!pid) {

    /* Handling builtins ran in background
     * (makes no sense but user knows best) */
    if ((exitcode = builtin_command(token)) >= 0)
      exit(exitcode);

    /* Restore deafult signals handlers */
    Signal(SIGTSTP, SIG_DFL);
    Signal(SIGTTIN, SIG_DFL);
    Signal(SIGTTOU, SIG_DFL);

    /* Unblock SIGCHLD in child */
    Sigprocmask(SIG_SETMASK, &mask, NULL);

    /* Redirect I/O */
    if (input != -1) {
      Dup2(input, STDIN_FILENO);
      Close(input);
    }
    if (output != -1) {
      Dup2(output, STDOUT_FILENO);
      Close(output);
    }

    /* Run command */
    external_command(token);
  }

  /* Close unused file descriptors */
  MaybeClose(&input);
  MaybeClose(&output);

  /* Register job and process */
  int job = addjob(pid, bg);
  addproc(job, pid, token);

  /* Monitor job if in foreground
   * else print msg on STDERR */
  if (!bg)
    exitcode = monitorjob(&mask);
  else
    msg("[%d] running '%s'\n", job, jobcmd(job));

  Sigprocmask(SIG_SETMASK, &mask, NULL);
  return exitcode;
}

/* Start internal or external command in a subprocess that belongs to pipeline.
 * All subprocesses in pipeline must belong to the same process group. */
static pid_t do_stage(pid_t pgid, sigset_t *mask, int input, int output,
                      token_t *token, int ntokens) {

  ntokens = do_redir(token, ntokens, &input, &output);

  if (ntokens == 0)
    app_error("ERROR: Command line is not well formed!");

  /* TODO: Start a subprocess and make sure it's moved to a process group. */
  pid_t pid = Fork();
  int exitcode = -1;

  /* If that's the first process being executed set its pgid to its pid
   * else set pgid of the process to pgid of first process in pipline */
  Setpgid(pid, pgid);

  /* Child */
  if (!pid) {
    /* Stop ignoring certain signals*/
    Signal(SIGTSTP, SIG_DFL);
    Signal(SIGTTIN, SIG_DFL);
    Signal(SIGTTOU, SIG_DFL);

    /* Unblock SIGCHLD */
    Sigprocmask(SIG_SETMASK, mask, NULL);

    /* If the process is builtin command there's no need to monitor
     * it -- just execute and exit with exitcode */
    if ((exitcode = builtin_command(token)) >= 0)
      exit(exitcode);

    /* Redirect I/O */
    if (input != -1) {
      Dup2(input, STDIN_FILENO);
      Close(input);
    }
    if (output != -1) {
      Dup2(output, STDOUT_FILENO);
      Close(output);
    }

    /* Run command */
    external_command(token);
  }

  debug("Running in pipe [%d] %s\n", pid, token[0]);
  return pid;
}

static void mkpipe(int *readp, int *writep) {
  int fds[2];
  Pipe(fds);
  fcntl(fds[0], F_SETFD, FD_CLOEXEC);
  fcntl(fds[1], F_SETFD, FD_CLOEXEC);
  *readp = fds[0];
  *writep = fds[1];
}

/* Pipeline execution creates a multiprocess job. Both internal and external
 * commands are executed in subprocesses. */
static int do_pipeline(token_t *token, int ntokens, bool bg) {
  pid_t pid, pgid = 0;
  int job = -1;
  int exitcode = 0;

  int input = -1, output = -1, next_input = -1;

  mkpipe(&next_input, &output);

  sigset_t mask;
  Sigprocmask(SIG_BLOCK, &sigchld_mask, &mask);

  /* TODO: Start pipeline subprocesses, create a job and monitor it.
   * Remember to close unused pipe ends! */
  int tokens_begining = 0, tokens_end;

  while (tokens_begining < ntokens) {

    /* Set boundries for tokens */
    for (tokens_end = tokens_begining;
         tokens_end != ntokens && token[tokens_end] != T_PIPE; tokens_end++) {
    }

    /* Last process in pipeline */
    if (tokens_end == ntokens) {
      input = next_input;
      output = -1;
    }

    /* Middle process in pipeline */
    else if (tokens_begining != 0) {
      input = next_input;
      mkpipe(&next_input, &output);
    }

    debug("INPUT: [%d], OUTPUT: [%d] NEXT INPUT: [%d]\n", input, output,
          next_input);

    pid = do_stage(pgid, &mask, input, output, token + tokens_begining,
                   tokens_end - tokens_begining);

    /* Close parent's pipe ends */
    MaybeClose(&input);
    MaybeClose(&output);

    /* Set the value of pgid to pid of the first process */
    if (pgid == 0) {
      pgid = pid;

      /* Job setup */
      job = addjob(pid, bg);
    }

    addproc(job, pid, token + tokens_begining);

    tokens_begining = tokens_end + 1;
  }

  /* Monitor job if in foreground
   * else print msg on STDERR */
  if (!bg)
    exitcode = monitorjob(&mask);
  else
    msg("[%d] running '%s'\n", job, jobcmd(job));

  Sigprocmask(SIG_SETMASK, &mask, NULL);
  return exitcode;
}

static bool is_pipeline(token_t *token, int ntokens) {
  for (int i = 0; i < ntokens; i++)
    if (token[i] == T_PIPE)
      return true;
  return false;
}

static void eval(char *cmdline) {
  bool bg = false;
  int ntokens;
  token_t *token = tokenize(cmdline, &ntokens);

  if (ntokens > 0 && token[ntokens - 1] == T_BGJOB) {
    token[--ntokens] = NULL;
    bg = true;
  }

  if (ntokens > 0) {
    if (is_pipeline(token, ntokens)) {
      do_pipeline(token, ntokens, bg);
    } else {
      do_job(token, ntokens, bg);
    }
  }

  free(token);
}

int main(int argc, char *argv[]) {
  rl_initialize();

  sigemptyset(&sigchld_mask);
  sigaddset(&sigchld_mask, SIGCHLD);

  if (getsid(0) != getpgid(0))
    Setpgid(0, 0);

  initjobs();

  Signal(SIGINT, sigint_handler);
  Signal(SIGTSTP, SIG_IGN);
  Signal(SIGTTIN, SIG_IGN);
  Signal(SIGTTOU, SIG_IGN);

  char *line;
  while (true) {
    if (!sigsetjmp(loop_env, 1)) {
      line = readline("# ");
    } else {
      msg("\n");
      continue;
    }

    if (line == NULL)
      break;

    if (strlen(line)) {
      add_history(line);
      eval(line);
    }
    free(line);
    watchjobs(FINISHED);
  }

  msg("\n");
  shutdownjobs();

  return 0;
}
