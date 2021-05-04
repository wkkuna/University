# Wydruki llvm-mca

- Dla $(0)$
```=
Iterations:        100000
Instructions:      2200000
Total Cycles:      1275037
Total uOps:        2800000

Dispatch Width:    6
uOps Per Cycle:    2.20
IPC:               1.73
Block RThroughput: 4.7


Instruction Info:
[1]: #uOps
[2]: Latency
[3]: RThroughput
[4]: MayLoad
[5]: MayStore
[6]: HasSideEffects (U)

[1]    [2]    [3]    [4]    [5]    [6]    Instructions:
 1      100   0.25                  U     endbr64
 1      1     0.25                        testq	%rsi, %rsi
 1      1     0.50                        jle	.L5
 1      0     0.17                        xorl	%eax, %eax
 1      1     0.50                        jmp	.L4
 1      1     0.17                        nopl	(%rax)
 1      1     0.50                        setl	%cl
 1      1     0.25                        movzbl	%cl, %ecx
 1      1     0.50                        leaq	1(%rcx,%rax,2), %rax
 1      1     0.25                        cmpq	%rax, %rsi
 1      1     0.50                        jle	.L5
 1      5     0.50    *                   movl	(%rdi,%rax,4), %ecx
 1      1     0.25                        cmpl	%edx, %ecx
 1      1     0.50                        jne	.L10
 1      1     0.25                        movl	$1, %eax
 3      7     1.00                  U     retq
 1      1     0.17                        nopl	(%rax)
 1      0     0.17                        xorl	%eax, %eax
 3      7     1.00                  U     retq
 1      1     0.17                  U     data16
 1      1     0.17                        nopw	%cs:(%rax,%rax)
 3      2     0.75                        xchgw	%ax, %ax


Resources:
[0]   - SKLDivider
[1]   - SKLFPDivider
[2]   - SKLPort0
[3]   - SKLPort1
[4]   - SKLPort2
[5]   - SKLPort3
[6]   - SKLPort4
[7]   - SKLPort5
[8]   - SKLPort6
[9]   - SKLPort7


Resource pressure per iteration:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    
 -      -     5.00   4.25   1.50   1.50    -     4.25   5.50    -     

Resource pressure by instruction:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    Instructions:
 -      -     0.13   0.38    -      -      -     0.12   0.38    -     endbr64
 -      -      -     0.25    -      -      -     0.25   0.50    -     testq	%rsi, %rsi
 -      -     0.50    -      -      -      -      -     0.50    -     jle	.L5
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -     0.50    -      -      -      -      -     0.50    -     jmp	.L4
 -      -      -      -      -      -      -      -      -      -     nopl	(%rax)
 -      -     0.25    -      -      -      -      -     0.75    -     setl	%cl
 -      -      -      -      -      -      -     1.00    -      -     movzbl	%cl, %ecx
 -      -      -     0.25    -      -      -     0.75    -      -     leaq	1(%rcx,%rax,2), %rax
 -      -     0.13   0.38    -      -      -     0.50    -      -     cmpq	%rax, %rsi
 -      -     0.75    -      -      -      -      -     0.25    -     jle	.L5
 -      -      -      -     0.50   0.50    -      -      -      -     movl	(%rdi,%rax,4), %ecx
 -      -     0.25   0.13    -      -      -     0.38   0.25    -     cmpl	%edx, %ecx
 -      -     0.62    -      -      -      -      -     0.38    -     jne	.L10
 -      -      -     0.87    -      -      -     0.13    -      -     movl	$1, %eax
 -      -     0.25   0.62   0.50   0.50    -     0.13   1.00    -     retq
 -      -      -      -      -      -      -      -      -      -     nopl	(%rax)
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -     0.13   0.62   0.50   0.50    -     0.25   1.00    -     retq
 -      -      -      -      -      -      -      -      -      -     data16
 -      -      -      -      -      -      -      -      -      -     nopw	%cs:(%rax,%rax)
 -      -     1.50   0.75    -      -      -     0.75    -      -     xchgw	%ax, %ax
```

- Dla $(1)$
```=
Iterations:        100000
Instructions:      2400000
Total Cycles:      1312540
Total uOps:        3000000

Dispatch Width:    6
uOps Per Cycle:    2.29
IPC:               1.83
Block RThroughput: 5.0


Instruction Info:
[1]: #uOps
[2]: Latency
[3]: RThroughput
[4]: MayLoad
[5]: MayStore
[6]: HasSideEffects (U)

[1]    [2]    [3]    [4]    [5]    [6]    Instructions:
 1      100   0.25                  U     endbr64
 1      1     0.25                        testq	%rsi, %rsi
 1      1     0.50                        jle	.L16
 1      0     0.17                        xorl	%eax, %eax
 1      1     0.50                        jmp	.L14
 1      1     0.17                        nopl	(%rax)
 1      1     0.25                        addq	$1, %rax
 1      1     0.25                        cmpl	%edx, %ecx
 1      1     0.50                        je	.L17
 1      1     0.25                        cmpq	%rax, %rsi
 1      1     0.50                        jle	.L16
 1      5     0.50    *                   movl	(%rdi,%rax,4), %ecx
 1      1     0.25                        addq	%rax, %rax
 1      1     0.25                        cmpl	%edx, %ecx
 1      1     0.50                        jge	.L19
 1      1     0.25                        addq	$2, %rax
 1      1     0.25                        cmpq	%rax, %rsi
 1      1     0.50                        jg	.L14
 1      0     0.17                        xorl	%eax, %eax
 3      7     1.00                  U     retq
 1      1     0.17                        nopl	(%rax,%rax)
 1      1     0.25                        movl	$1, %eax
 3      7     1.00                  U     retq
 3      2     0.75                        xchgw	%ax, %ax


Resources:
[0]   - SKLDivider
[1]   - SKLFPDivider
[2]   - SKLPort0
[3]   - SKLPort1
[4]   - SKLPort2
[5]   - SKLPort3
[6]   - SKLPort4
[7]   - SKLPort5
[8]   - SKLPort6
[9]   - SKLPort7


Resource pressure per iteration:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    
 -      -     6.00   5.25   1.50   1.50    -     5.75   6.00    -     

Resource pressure by instruction:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    Instructions:
 -      -     0.50    -      -      -      -     0.50    -      -     endbr64
 -      -     0.13   0.50    -      -      -      -     0.38    -     testq	%rsi, %rsi
 -      -     0.25    -      -      -      -      -     0.75    -     jle	.L16
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -     0.50    -      -      -      -      -     0.50    -     jmp	.L14
 -      -      -      -      -      -      -      -      -      -     nopl	(%rax)
 -      -      -     0.37    -      -      -     0.38   0.25    -     addq	$1, %rax
 -      -      -     0.37    -      -      -     0.62    -      -     cmpl	%edx, %ecx
 -      -     1.00    -      -      -      -      -      -      -     je	.L17
 -      -      -     0.62    -      -      -     0.38    -      -     cmpq	%rax, %rsi
 -      -      -      -      -      -      -      -     1.00    -     jle	.L16
 -      -      -      -     0.50   0.50    -      -      -      -     movl	(%rdi,%rax,4), %ecx
 -      -      -      -      -      -      -     0.37   0.62    -     addq	%rax, %rax
 -      -     0.37   0.13    -      -      -     0.50    -      -     cmpl	%edx, %ecx
 -      -     1.00    -      -      -      -      -      -      -     jge	.L19
 -      -      -     0.25    -      -      -     0.75    -      -     addq	$2, %rax
 -      -      -     0.37    -      -      -     0.63    -      -     cmpq	%rax, %rsi
 -      -     0.50    -      -      -      -      -     0.50    -     jg	.L14
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -      -     0.63   0.50   0.50    -     0.37   1.00    -     retq
 -      -      -      -      -      -      -      -      -      -     nopl	(%rax,%rax)
 -      -     0.62   0.38    -      -      -      -      -      -     movl	$1, %eax
 -      -      -     0.13   0.50   0.50    -     0.87   1.00    -     retq
 -      -     1.12   1.50    -      -      -     0.38    -      -     xchgw	%ax, %ax
```

- Dla $(2)$
```=
Iterations:        100000
Instructions:      1900000
Total Cycles:      1040040
Total uOps:        2400000

Dispatch Width:    6
uOps Per Cycle:    2.31
IPC:               1.83
Block RThroughput: 4.0


Instruction Info:
[1]: #uOps
[2]: Latency
[3]: RThroughput
[4]: MayLoad
[5]: MayStore
[6]: HasSideEffects (U)

[1]    [2]    [3]    [4]    [5]    [6]    Instructions:
 1      100   0.25                  U     endbr64
 1      1     0.25                        testq	%rsi, %rsi
 1      1     0.50                        jle	.L24
 1      0     0.17                        xorl	%eax, %eax
 1      1     0.50                        jmp	.L23
 1      1     0.17                        nopl	(%rax)
 1      1     0.50                        setl	%al
 1      1     0.25                        movzbl	%al, %eax
 1      1     0.50                        leaq	1(%rax,%rcx), %rax
 1      1     0.25                        cmpq	%rax, %rsi
 1      1     0.50                        jle	.L24
 1      1     0.50                        leaq	(%rax,%rax), %rcx
 2      6     0.50    *                   cmpl	%edx, (%rdi,%rax,4)
 1      1     0.50                        jne	.L28
 1      1     0.25                        movl	$1, %eax
 3      7     1.00                  U     retq
 1      1     0.17                        nop
 1      0     0.17                        xorl	%eax, %eax
 3      7     1.00                  U     retq


Resources:
[0]   - SKLDivider
[1]   - SKLFPDivider
[2]   - SKLPort0
[3]   - SKLPort1
[4]   - SKLPort2
[5]   - SKLPort3
[6]   - SKLPort4
[7]   - SKLPort5
[8]   - SKLPort6
[9]   - SKLPort7


Resource pressure per iteration:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    
 -      -     4.70   3.70   1.50   1.50    -     3.90   4.70    -     

Resource pressure by instruction:
[0]    [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]    Instructions:
 -      -     0.40   0.40    -      -      -      -     0.20    -     endbr64
 -      -     0.20   0.40    -      -      -     0.40    -      -     testq	%rsi, %rsi
 -      -     0.70    -      -      -      -      -     0.30    -     jle	.L24
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -     0.60    -      -      -      -      -     0.40    -     jmp	.L23
 -      -      -      -      -      -      -      -      -      -     nopl	(%rax)
 -      -     0.20    -      -      -      -      -     0.80    -     setl	%al
 -      -      -     0.40    -      -      -     0.50   0.10    -     movzbl	%al, %eax
 -      -      -     0.80    -      -      -     0.20    -      -     leaq	1(%rax,%rcx), %rax
 -      -      -     0.10    -      -      -     0.90    -      -     cmpq	%rax, %rsi
 -      -     0.50    -      -      -      -      -     0.50    -     jle	.L24
 -      -      -     0.90    -      -      -     0.10    -      -     leaq	(%rax,%rax), %rcx
 -      -     0.80    -     0.60   0.40    -      -     0.20    -     cmpl	%edx, (%rdi,%rax,4)
 -      -     0.90    -      -      -      -      -     0.10    -     jne	.L28
 -      -      -     0.30    -      -      -     0.60   0.10    -     movl	$1, %eax
 -      -     0.40   0.20   0.50   0.50    -     0.40   1.00    -     retq
 -      -      -      -      -      -      -      -      -      -     nop
 -      -      -      -      -      -      -      -      -      -     xorl	%eax, %eax
 -      -      -     0.20   0.40   0.60    -     0.80   1.00    -     retq
```
