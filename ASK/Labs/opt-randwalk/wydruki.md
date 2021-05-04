# Wydruki dla randwalk0 randwalk1

```=
00000000000027f0 <randwalk0>:
    27f0:	f3 0f 1e fa          	endbr64 
    27f4:	41 57                	push   %r15
    27f6:	31 c0                	xor    %eax,%eax
    27f8:	41 89 f7             	mov    %esi,%r15d
    27fb:	31 c9                	xor    %ecx,%ecx
    27fd:	41 56                	push   %r14
    27ff:	49 89 fe             	mov    %rdi,%r14
    2802:	8d 7e ff             	lea    -0x1(%rsi),%edi
    2805:	41 55                	push   %r13
    2807:	45 31 ed             	xor    %r13d,%r13d
    280a:	41 54                	push   %r12
    280c:	41 89 d4             	mov    %edx,%r12d
    280f:	55                   	push   %rbp
    2810:	89 f5                	mov    %esi,%ebp
    2812:	53                   	push   %rbx
    2813:	c1 ed 1f             	shr    $0x1f,%ebp
    2816:	01 f5                	add    %esi,%ebp
    2818:	d1 fd                	sar    %ebp
    281a:	48 83 ec 18          	sub    $0x18,%rsp
    281e:	89 eb                	mov    %ebp,%ebx
    2820:	89 7c 24 0c          	mov    %edi,0xc(%rsp)
    2824:	eb 1a                	jmp    2840 <randwalk0+0x50>
    2826:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
    282d:	00 00 00 
    2830:	31 f6                	xor    %esi,%esi
    2832:	85 ed                	test   %ebp,%ebp
*** 2834:	40 0f 9f c6          	setg   %sil
    2838:	29 f5                	sub    %esi,%ebp
    283a:	41 83 ec 01          	sub    $0x1,%r12d
*** 283e:	74 44                	je     2884 <randwalk0+0x94>
    2840:	83 e9 02             	sub    $0x2,%ecx
*** 2843:	78 5b                	js     28a0 <randwalk0+0xb0>
    2845:	41 89 e8             	mov    %ebp,%r8d
    2848:	49 89 c1             	mov    %rax,%r9
    284b:	45 0f af c7          	imul   %r15d,%r8d
    284f:	49 d3 e9             	shr    %cl,%r9
    2852:	41 01 d8             	add    %ebx,%r8d
    2855:	4d 63 c0             	movslq %r8d,%r8
    2858:	43 0f b6 34 06       	movzbl (%r14,%r8,1),%esi
    285d:	41 01 f5             	add    %esi,%r13d
    2860:	41 83 e1 03          	and    $0x3,%r9d
*** 2864:	74 ca                	je     2830 <randwalk0+0x40>
    2866:	41 83 f9 01          	cmp    $0x1,%r9d
*** 286a:	74 44                	je     28b0 <randwalk0+0xc0>
    286c:	41 83 f9 02          	cmp    $0x2,%r9d
*** 2870:	74 56                	je     28c8 <randwalk0+0xd8>
    2872:	31 f6                	xor    %esi,%esi
    2874:	39 5c 24 0c          	cmp    %ebx,0xc(%rsp)
*** 2878:	40 0f 9f c6          	setg   %sil
    287c:	01 f3                	add    %esi,%ebx
    287e:	41 83 ec 01          	sub    $0x1,%r12d
*** 2882:	75 bc                	jne    2840 <randwalk0+0x50>
    2884:	48 83 c4 18          	add    $0x18,%rsp
    2888:	44 89 e8             	mov    %r13d,%eax
    288b:	5b                   	pop    %rbx
    288c:	5d                   	pop    %rbp
    288d:	41 5c                	pop    %r12
    288f:	41 5d                	pop    %r13
    2891:	41 5e                	pop    %r14
    2893:	41 5f                	pop    %r15
    2895:	c3                   	retq   
    2896:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
    289d:	00 00 00 
    28a0:	31 c0                	xor    %eax,%eax
    28a2:	e8 d9 03 00 00       	callq  2c80 <fast_random>
    28a7:	b9 3e 00 00 00       	mov    $0x3e,%ecx
    28ac:	eb 97                	jmp    2845 <randwalk0+0x55>
    28ae:	66 90                	xchg   %ax,%ax
    28b0:	31 f6                	xor    %esi,%esi
    28b2:	39 6c 24 0c          	cmp    %ebp,0xc(%rsp)
*** 28b6:	40 0f 9f c6          	setg   %sil
    28ba:	01 f5                	add    %esi,%ebp
    28bc:	e9 79 ff ff ff       	jmpq   283a <randwalk0+0x4a>
    28c1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
    28c8:	31 f6                	xor    %esi,%esi
    28ca:	85 db                	test   %ebx,%ebx
*** 28cc:	40 0f 9f c6          	setg   %sil
    28d0:	29 f3                	sub    %esi,%ebx
    28d2:	e9 63 ff ff ff       	jmpq   283a <randwalk0+0x4a>
    28d7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
    28de:	00 00 
```


```=
00000000000028e0 <randwalk1>:
    28e0:	f3 0f 1e fa          	endbr64 
    28e4:	41 57                	push   %r15
    28e6:	31 c0                	xor    %eax,%eax
    28e8:	41 89 f7             	mov    %esi,%r15d
    28eb:	31 c9                	xor    %ecx,%ecx
    28ed:	41 56                	push   %r14
    28ef:	49 89 fe             	mov    %rdi,%r14
    28f2:	41 55                	push   %r13
    28f4:	45 31 ed             	xor    %r13d,%r13d
    28f7:	41 54                	push   %r12
    28f9:	41 89 d4             	mov    %edx,%r12d
    28fc:	8d 56 ff             	lea    -0x1(%rsi),%edx
    28ff:	55                   	push   %rbp
    2900:	53                   	push   %rbx
    2901:	89 f3                	mov    %esi,%ebx
    2903:	c1 eb 1f             	shr    $0x1f,%ebx
    2906:	01 f3                	add    %esi,%ebx
    2908:	d1 fb                	sar    %ebx
    290a:	48 83 ec 18          	sub    $0x18,%rsp
    290e:	89 dd                	mov    %ebx,%ebp
    2910:	eb 7a                	jmp    298c <randwalk1+0xac>
    2912:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    2918:	41 89 d9             	mov    %ebx,%r9d
    291b:	49 89 c0             	mov    %rax,%r8
    291e:	45 0f af cf          	imul   %r15d,%r9d
    2922:	49 d3 e8             	shr    %cl,%r8
    2925:	41 01 e9             	add    %ebp,%r9d
    2928:	4d 63 c9             	movslq %r9d,%r9
    292b:	43 0f b6 34 0e       	movzbl (%r14,%r9,1),%esi
    2930:	41 01 f5             	add    %esi,%r13d
    2933:	41 83 e0 03          	and    $0x3,%r8d
*** 2937:	40 0f 94 c7          	sete   %dil
    293b:	31 f6                	xor    %esi,%esi
    293d:	85 db                	test   %ebx,%ebx
*** 293f:	40 0f 9f c6          	setg   %sil
    2943:	21 fe                	and    %edi,%esi
    2945:	29 f3                	sub    %esi,%ebx
    2947:	41 83 f8 01          	cmp    $0x1,%r8d
*** 294b:	40 0f 94 c7          	sete   %dil
    294f:	31 f6                	xor    %esi,%esi
    2951:	39 d3                	cmp    %edx,%ebx
*** 2953:	40 0f 9c c6          	setl   %sil
    2957:	21 fe                	and    %edi,%esi
    2959:	01 f3                	add    %esi,%ebx
    295b:	41 83 f8 02          	cmp    $0x2,%r8d
*** 295f:	40 0f 94 c7          	sete   %dil
    2963:	31 f6                	xor    %esi,%esi
    2965:	85 ed                	test   %ebp,%ebp
*** 2967:	40 0f 9f c6          	setg   %sil
    296b:	21 fe                	and    %edi,%esi
    296d:	29 f5                	sub    %esi,%ebp
    296f:	41 83 f8 02          	cmp    $0x2,%r8d
*** 2973:	40 0f 97 c6          	seta   %sil
    2977:	45 31 c0             	xor    %r8d,%r8d
    297a:	39 d5                	cmp    %edx,%ebp
*** 297c:	41 0f 9c c0          	setl   %r8b
    2980:	41 21 f0             	and    %esi,%r8d
    2983:	44 01 c5             	add    %r8d,%ebp
    2986:	41 83 ec 01          	sub    $0x1,%r12d
*** 298a:	74 24                	je     29b0 <randwalk1+0xd0>
    298c:	83 e9 02             	sub    $0x2,%ecx
*** 298f:	79 87                	jns    2918 <randwalk1+0x38>
    2991:	31 c0                	xor    %eax,%eax
    2993:	89 54 24 0c          	mov    %edx,0xc(%rsp)
    2997:	e8 04 03 00 00       	callq  2ca0 <fast_random>
    299c:	8b 54 24 0c          	mov    0xc(%rsp),%edx
    29a0:	b9 3e 00 00 00       	mov    $0x3e,%ecx
    29a5:	e9 6e ff ff ff       	jmpq   2918 <randwalk1+0x38>
    29aa:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    29b0:	48 83 c4 18          	add    $0x18,%rsp
    29b4:	44 89 e8             	mov    %r13d,%eax
    29b7:	5b                   	pop    %rbx
    29b8:	5d                   	pop    %rbp
    29b9:	41 5c                	pop    %r12
    29bb:	41 5d                	pop    %r13
    29bd:	41 5e                	pop    %r14
    29bf:	41 5f                	pop    %r15
    29c1:	c3                   	retq   
    29c2:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
    29c9:	00 00 00 
    29cc:	0f 1f 40 00          	nopl   0x0(%rax)
```

###### tags: `ask`