	.text
	.globl	clz
	.type	clz, @function

clz:
	# x | x >> (count)
	# doing this for 1, 2, 4, 8, 16, 32 
	# the most significant 1 is 'spread' 
	# onto the lower bits
	# ex. 0001010110.. becomes 0001111111.. 
	# if we bitwise NOT this number we 
	# set all bits that were previously zero to one
	# then the only thing left to do is count those bits
	movq %rdi, %rsi
	shrq $1, %rsi
	orq  %rsi, %rdi

	movq %rdi, %rcx
	shrq $2, %rdi
	orq  %rdi, %rcx 

	movq %rcx, %r9
	shrq $4, %r9
	orq  %rcx, %r9 

	movq %r9, %r10
	shrq $8, %r10
	orq  %r9, %r10

	movq %r10, %r11
	shrq $16, %r11
	orq  %r10, %r11

	movq %r11, %rax
	shrq $32, %rax
	orq  %r11, %rax

	not %rax

	# popcount 

	# 0x5555555555555555  = 0101...
	# 0x3333333333333333  = 0011...
	# 0x0f0f0f0f0f0f0f0f  = 00001111...
	
	# x -= (x>>1) & 0x5555555555555555
	movq %rax, %rdi
	shrq $1, %rdi
	movq $0x5555555555555555, %r11
	andq %r11, %rdi
	subq %rdi, %rax

	# x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
	movq %rax, %rcx 
	shrq $2, %rcx
	movq $0x3333333333333333, %r10
	andq %r10, %rcx

	andq %r10, %rax
	addq %rax, %rcx

	# x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
	movq $0x0f0f0f0f0f0f0f0f, %r11
	movq %rcx, %rsi 
	shrq $4, %rsi
	addq %rcx, %rsi
	andq %r11, %rsi

	# x += x >>  8
	movq %rsi, %r10
	shrq $8, %r10
	addq %rsi, %r10

	# x += x >> 16
	movq %r10, %r8
	shrq $16, %r8
	addq %r10, %r8

	# x += x >> 32
	movq %r8, %rax
	shrq $32, %rax
	addq %r8, %rax 

	# x & 0xtf 
	andq $0x7f, %rax 

	ret

	.size	clz, .-clz
