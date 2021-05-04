        .text
        .globl  addsb
        .type   addsb, @function

addsb:  
        # %rdi -> v1
        # %rsi -> v2
        movq    $0x8080808080808080, %r11      # mask: 1000 0000 1000...
        movq    $0x7F7F7F7F7F7F7F7F, %r10       # mask: 0111 1111 0111...
        
        movq    %rsi, %rax
        xorq    %rdi, %rax
        andq    %r11, %rax # different signs

        movq    %rdi, %rcx
        andq    %rsi, %rcx # both negative
        
        movq    %rdi, %r9
        orq     %rsi, %r9
        not     %r9
        andq    %r11, %r9   # both positive

        # removing sgn and adding values together:
        andq    %r10, %rdi
        andq    %r10, %rsi
        addq    %rdi, %rsi  # add after sgn bit removal

        # two negative & overflow:
        movq    %rsi, %r8
        not     %r8
        andq    %r8, %rcx   # if neg & neg and sgn bit after addition = 0
        andq    %r11, %rcx
        movq    %rcx, %rdi  # part of result; sum < -128 case
        movq    %rcx, %rdx  # part of mask (future)
        
        # two positive & overflow
        andq    %rsi, %r9   # case sum > 127
        orq     %r9, %rdx   # sgn-bit = 1 if any overflow
        shrq    $7, %r9     # set sgn on idx 0
        movq    %r11, %rcx
        subq    %r9, %rcx   # 0111 1111 - for overflow
                            # 1000 0000 - otherwise
        andq    %r10, %rcx  # clean up sgn
        orq     %rcx, %rdi  # add this case to result

        # mask to erase overflows:
        movq    %r11, %r8
        shrq    $7, %rdx   # overflows on idx 0
        subq    %rdx, %r8  # 0111 1111 - for overflows
                           # 1000 0000 - otherwise
        xorq    %r11, %r8  # 1111 1111 - for overflows
                           # 0000 0000 - otherwise
        not     %r8        # other way round

        andq    %r8, %rsi  # extracting only operations in range
        xorq    %rsi, %rax
        orq     %rdi, %rax # complementing result
        ret

        .size   addsb, .-addsb
