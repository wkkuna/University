#define DEBUG 0
#include "shell.h"

typedef struct proc {
  pid_t pid;    /* process identifier */
  int state;    /* RUNNING or STOPPED or FINISHED */
  int exitcode; /* -1 if exit status not yet received */
} proc_t;

typedef struct job {
  pid_t pgid;            /* 0 if slot is free */
  proc_t *proc;          /* array of processes running in as a job */
  struct termios tmodes; /* saved terminal modes */
  int nproc;             /* number of processes */
  int state;             /* changes when live processes have same state */
  char *command;         /* textual representation of command line */
} job_t;

static job_t *jobs = NULL;          /* array of all jobs */
static int njobmax = 1;             /* number of slots in jobs array */
static int tty_fd = -1;             /* controlling terminal file descriptor */
static struct termios shell_tmodes; /* saved shell terminal modes */

static void sigchld_handler(int sig) {
  int old_errno = errno;
  pid_t pid;
  int status;
  /* TODO: Change state (FINISHED, RUNNING, STOPPED) of processes and jobs.
   * Bury all children that finished saving their status in jobs. */

    
  /* Several signals can be delivered in one block, so we're executing
   * until no child has anything to report or there's no children left */
  while ((pid = waitpid(WAIT_ANY, &status, WUNTRACED | WCONTINUED | WNOHANG)) >
         0) {

    /* Helpful pointers that don't make code more spaghetti
     * than it already is */
    job_t *job = NULL;
    proc_t *proc = NULL;
    int state = -1, nproc = -1;

    /* Find job & process reporting their state */
    for (int i = 0; i < njobmax; i++) {
      nproc = jobs[i].nproc;
      for (int j = 0; j < nproc; j++) {
        if (jobs[i].proc[j].pid == pid) {
          job = &jobs[i];
          proc = &(job->proc[j]);
          break;
        }
      }
    }

    assert(job != NULL && proc != NULL);

    /* Change the state of a process accordingly to recieved signal */

    /* Child stopped */
    if (WIFSTOPPED(status)) {
      proc->state = STOPPED;
      state = STOPPED;
      debug("\nPROCESS STOPPED: [%d]\n", pid);
    }

    /* Child resumed */
    else if (WIFCONTINUED(status)) {
      proc->state = RUNNING;
      state = RUNNING;
      debug("\nPROCESS CONTINUED: [%d]\n", pid);
    }

    /* Set exit status for the ones who exited */

    /* Child recived signal x.x */
    else if (WIFSIGNALED(status)) {
      proc->state = FINISHED;
      state = FINISHED;
      proc->exitcode = status;
      debug("\nPROCESS KILLED BY SIGNAL: [%d]\n", pid);
    }

    /* Child finished normally */
    else if (WIFEXITED(status)) {
      proc->state = FINISHED;
      state = FINISHED;
      proc->exitcode = status;
      debug("\nPROCESS EXITED: [%d], \n", pid);
    }

    /* Check if job's state needs to be updated */

    int j = 0;
    while ((j < nproc) && (job->proc[j].state == state)) {
      j++;
    }
    if (j == nproc)
      job->state = state;
  }

  errno = old_errno;
}

/* When pipeline is done, its exitcode is fetched from the last process. */
static int exitcode(job_t *job) {
  return job->proc[job->nproc - 1].exitcode;
}

static int allocjob(void) {
  /* Find empty slot for background job. */
  for (int j = BG; j < njobmax; j++)
    if (jobs[j].pgid == 0)
      return j;

  /* If none found, allocate new one. */
  jobs = realloc(jobs, sizeof(job_t) * (njobmax + 1));
  memset(&jobs[njobmax], 0, sizeof(job_t));
  return njobmax++;
}

static int allocproc(int j) {
  job_t *job = &jobs[j];
  job->proc = realloc(job->proc, sizeof(proc_t) * (job->nproc + 1));
  return job->nproc++;
}

int addjob(pid_t pgid, int bg) {
  int j = bg ? allocjob() : FG;
  job_t *job = &jobs[j];
  /* Initial state of a job. */
  job->pgid = pgid;
  job->state = RUNNING;
  job->command = NULL;
  job->proc = NULL;
  job->nproc = 0;
  job->tmodes = shell_tmodes;
  return j;
}

static void deljob(job_t *job) {
  assert(job->state == FINISHED);
  free(job->command);
  free(job->proc);
  job->pgid = 0;
  job->command = NULL;
  job->proc = NULL;
  job->nproc = 0;
}

static void movejob(int from, int to) {
  assert(jobs[to].pgid == 0);
  memcpy(&jobs[to], &jobs[from], sizeof(job_t));
  memset(&jobs[from], 0, sizeof(job_t));
}

static void mkcommand(char **cmdp, char **argv) {
  if (*cmdp)
    strapp(cmdp, " | ");

  for (strapp(cmdp, *argv++); *argv; argv++) {
    strapp(cmdp, " ");
    strapp(cmdp, *argv);
  }
}

void addproc(int j, pid_t pid, char **argv) {
  assert(j < njobmax);
  job_t *job = &jobs[j];

  int p = allocproc(j);
  proc_t *proc = &job->proc[p];
  /* Initial state of a process. */
  proc->pid = pid;
  proc->state = RUNNING;
  proc->exitcode = -1;
  mkcommand(&job->command, argv);
}

/* Returns job's state.
 * If it's finished, delete it and return exitcode through statusp. */
int jobstate(int j, int *statusp) {
  assert(j < njobmax);
  job_t *job = &jobs[j];
  int state = job->state;

  /* TODO: Handle case where job has finished. */

  /* Delete job if it's finished */
  if (state == FINISHED) {
    *statusp = exitcode(job);
    deljob(job);
  }

  return state;
}

char *jobcmd(int j) {
  assert(j < njobmax);
  job_t *job = &jobs[j];
  return job->command;
}

/* Continues a job that has been stopped. If move to foreground was requested,
 * then move the job to foreground and start monitoring it. */
bool resumejob(int j, int bg, sigset_t *mask) {
  if (j < 0) {
    for (j = njobmax - 1; j > 0 && jobs[j].state == FINISHED; j--)
      continue;
  }

  if (j >= njobmax || jobs[j].state == FINISHED)
    return false;

  /* TODO: Continue stopped job. Possibly move job to foreground slot. */

  /* Inform about resuming a job */
  msg("continue '%s'\n", jobcmd(j));

  /* Send SIGCONT to all processes in group of job's pgid */
  Kill(-jobs[j].pgid, SIGCONT);

  /* Make sure the job is running before monitoring it */
  while (jobs[j].state != RUNNING)
    Sigsuspend(mask);

  /* If job is meant to continiue to run in foregroud move it to fg
   * and monitor it */
  if (!bg) {
    movejob(j, 0);
    monitorjob(mask);
  }
  return true;
}

/* Kill the job by sending it a SIGTERM. */
bool killjob(int j) {
  if (j >= njobmax || jobs[j].state == FINISHED)
    return false;
  debug("[%d] killing '%s'\n", j, jobs[j].command);

  /* TODO: I love the smell of napalm in the morning. */
  /* It smells like victory... */

  /* Kill every process in group of job's pgid and send
   * SIGCONT when they're stopped so they can handle it */
  Kill(-jobs[j].pgid, SIGTERM);

  if (jobs[j].state == STOPPED)
    Kill(-jobs[j].pgid, SIGCONT);

  return true;
}

/* Report state of requested background jobs. Clean up finished jobs. */
void watchjobs(int which) {
  for (int j = BG; j < njobmax; j++) {
    if (jobs[j].pgid == 0)
      continue;

    /* TODO: Report job number, state, command and exit code or signal. */

    if (jobs[j].state != which && which != ALL)
      continue;

    int status;
    char *cmd = jobs[j].command;

    /* Apropriately report the state of the job */
    switch (jobs[j].state) {

      case RUNNING:
        msg("[%d] running '%s'\n", j, cmd);
        break;

      case STOPPED:
        msg("[%d] suspended '%s'\n", j, cmd);
        break;

      case FINISHED:
        status = exitcode(&jobs[j]);

        if (WIFSIGNALED(status))
          msg("[%d] killed '%s' by signal %d\n", j, cmd, WTERMSIG(status));

        else if (WIFEXITED(status))
          msg("[%d] exited '%s', status=%d\n", j, cmd, WEXITSTATUS(status));

        deljob(&jobs[j]);
        break;

      default:
        app_error("Ilegal process state!\n");
    }
  }
}

/* Monitor job execution. If it gets stopped move it to background.
 * When a job has finished or has been stopped move shell to foreground. */
int monitorjob(sigset_t *mask) {
  int exitcode = 0;

  /* TODO: Following code requires use of Tcsetpgrp of tty_fd. */

  assert(jobs[0].state == RUNNING);

  /* Save terminal modes and give control of the terminal to current job */
  Tcgetattr(tty_fd, &shell_tmodes);
  Tcsetpgrp(tty_fd, jobs[0].pgid);

  int state;

  /* Wait until a job is stopped or finished */
  while ((state = jobstate(0, &exitcode)) == RUNNING)
    Sigsuspend(mask);

  if (state == STOPPED) {
    /* Allocate a spot for a job and move it to the background */
    int job = allocjob();
    movejob(0, job);
    msg("[%d]+ Stopped %s\n", job, jobs[job].command);
  }

  /* Move shell to foreground when a job has stopped or finished
   * and restore saved terminal modes */
  Tcsetpgrp(tty_fd, getpgid(0));
  Tcsetattr(tty_fd, TCSANOW, &shell_tmodes);

  return WEXITSTATUS(exitcode);
}

/* Called just at the beginning of shell's life. */
void initjobs(void) {
  Signal(SIGCHLD, sigchld_handler);
  jobs = calloc(sizeof(job_t), 1);

  /* Assume we're running in interactive mode, so move us to foreground.
   * Duplicate terminal fd, but do not leak it to subprocesses that execve. */
  assert(isatty(STDIN_FILENO));
  tty_fd = Dup(STDIN_FILENO);
  fcntl(tty_fd, F_SETFD, FD_CLOEXEC);

  /* Take control of the terminal. */
  Tcsetpgrp(tty_fd, getpgrp());

  /* Save default terminal attributes for the shell. */
  Tcgetattr(tty_fd, &shell_tmodes);
}

/* Called just before the shell finishes. */
void shutdownjobs(void) {
  sigset_t mask;
  Sigprocmask(SIG_BLOCK, &sigchld_mask, &mask);

  /* TODO: Kill remaining jobs and wait for them to finish. */

  for (int i = BG; i < njobmax; i++) {

    /* Do not overwrite exit status if process already exited*/
    if (jobs[i].state == FINISHED)
      continue;

    killjob(i);

    /* Wait until the SIGTERM is handled */
    while (jobs[i].state != FINISHED)
      Sigsuspend(&mask);
  }

  watchjobs(FINISHED);

  Sigprocmask(SIG_SETMASK, &mask, NULL);

  Close(tty_fd);
}
