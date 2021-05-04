	.text
	.globl	mod17
	.type	mod17, @function

mod17:
# separate even from odds
	movq %rdi, %rsi
	movq $0x0f0f0f0f0f0f0f0f, %r8
	andq %r8, %rdi		# even
	shrq $4, %rsi
	andq %r8, %rsi		# odd

# add up each nibble
	# odd 
	movq %rsi, %rdx
	shrq $8,%rdx
	addq %rsi, %rdx

# add up each 2 nibbles
	# odd
	movq %rdx, %r11
	shrq $16, %rdx
	addq %rdx, %r11

# add up each all nibbles
	# odd
	movq %r11, %rsi
	shrq $32, %r11
	add %r11, %rsi

# add up each nibble
	# even
	movq %rdi, %r10
	shrq $8,%rdi
	addq %rdi, %r10

# add up each 2 nibbles
	# even
	movq %r10, %r8
	shrq $16, %r10
	addq %r10, %r8

# add up each all nibbles
	# even
	movq %r8, %rdi
	shrq $32, %r8
	add %r8, %rdi

	cmpb %dil, %sil
	sbb %edi, %esi			# substract sum of evens from sum of odds
							# substract 1 if overflowed

	mov %esi, %eax
	shr $4, %eax
	and $0xf, %eax
	and $0xf, %esi
	sub %esi, %eax			# substract even from odds

	sbb %r11d, %r11d
	and $0x11, %r11d
	add %r11d, %eax			# add 17 if negative
	ret

	.size	mod17, .-mod17
