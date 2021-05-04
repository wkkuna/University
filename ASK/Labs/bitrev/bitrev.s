.text
	.globl	bitrev
	.type	bitrev, @function

bitrev:
# First, let's reverse bytes
# A B C D E F G H ->  H G F E D C B A
        movq %rdi, %rcx
        rolw $8, %di       # A B C D E F H G
        roll $16, %edi     # A B C D H G E F  ## 0000 H.. if IA-32 
        rolw $8, %di       # A B C D H G F E  ## 0000 H.. if IA-32
        shlq $32, %rdi     # H G F E 0 0 0 0

        shrq $32, %rcx     # 0 0 0 0 A B C D
        rolw $8, %cx       # 0 0 0 0 A B D C
        roll $16, %ecx     # 0 0 0 0 D C A B
        rolw $8, %cx 	   # 0 0 0 0 D C B A
        orq %rcx, %rdi     # H G F E D C B A
# Then reverse bits in each byte
# 7 6 5 4 3 2 1 0 -> 3 2 1 0 7 6 5 4
        movq %rdi, %rax
        movq $0xF0F0F0F0F0F0F0F0, %r10 # 1111 0000... # 'and' allows up to 32-bit const.
        andq %r10, %rdi
        shrq $4, %rdi
        shlq $4, %rax
        andq %r10, %rax
        orq  %rdi, %rax

# 3 2 1 0 7 6 5 4 -> 1 0 3 2 5 4 7 6
        movq %rax, %r11
        movq $0x3333333333333333, %r10 # 0011 0011...
        andq %r10, %rax
        shlq $2, %rax
        shrq $2, %r11
        andq %r10, %r11
        orq  %r11, %rax

# 1 0 3 2 5 4 7 6 -> 0 1 2 3 4 5 6 7
        movq %rax, %rdx
        movq $0xAAAAAAAAAAAAAAAA, %r10 # 1010 1010...
        andq %r10, %rdx
        shrq $1, %rdx
        shlq $1, %rax
        andq %r10, %rax
        orq  %rdx, %rax
# Being given a number with bits: 63 62 61 ... 1 0
# Reversed bytes: 7 6 .. 0 | 15 ... 8 | ... | 63 ... 56
# Reversed bits:  0 ... 6 7 | 8 ... 15 | ... | 56 ... 63
	ret

	.size	bitrev, .-bitrev
