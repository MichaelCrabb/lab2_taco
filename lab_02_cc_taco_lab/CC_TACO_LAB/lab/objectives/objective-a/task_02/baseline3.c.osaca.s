	.file	"baseline3.c"
	.text
	.p2align 4
	.globl	compute_model_tst
	.type	compute_model_tst, @function
compute_model_tst:
.LFB27:
	.cfi_startproc
	endbr64
	movl	(%rsi), %eax
	vxorps	%xmm0, %xmm0, %xmm0
	vcvtsi2ssl	%eax, %xmm0, %xmm1
	leal	(%rax,%rax,2), %eax
	cltq
	salq	$2, %rax
	js	.L2
	vcvtsi2ssq	%rax, %xmm0, %xmm0
	vunpcklps	%xmm0, %xmm1, %xmm1
	vmovlps	%xmm1, (%rdi)
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	shrq	%rax
	vcvtsi2ssq	%rax, %xmm0, %xmm0
	vaddss	%xmm0, %xmm0, %xmm0
	vunpcklps	%xmm0, %xmm1, %xmm1
	vmovlps	%xmm1, (%rdi)
	ret
	.cfi_endproc
.LFE27:
	.size	compute_model_tst, .-compute_model_tst
	.p2align 4
	.globl	compute_tst
	.type	compute_tst, @function
compute_tst:
.LFB28:
	.cfi_startproc
	endbr64
	movl	(%rdi), %r9d
	movq	16(%rcx), %rcx
	movq	24(%rsi), %rdi
	movq	32(%rsi), %rsi
#APP
# 32 "baseline3.c" 1
	
	 movl    $111,%ebx #IACA/OSACA START MARKER
	 .byte   100,103,144     #IACA/OSACA START MARKER
# 0 "" 2
#NO_APP
	movl	$32, %edx
	xorl	%r8d, %r8d
	testl	%r9d, %r9d
	jle	.L7
	.p2align 4,,10
	.p2align 3
.L6:
	leaq	-32(%rdx), %rax
	.p2align 4,,10
	.p2align 3
.L8:
	vmovss	(%rdi,%rax), %xmm0
	vmulss	(%rsi,%rax), %xmm0, %xmm0
	vmovss	%xmm0, (%rcx,%rax)
	addq	$4, %rax
	cmpq	%rax, %rdx
	jne	.L8
	addl	$8, %r8d
	addq	$32, %rdx
	cmpl	%r8d, %r9d
	jg	.L6
.L7:
#APP
# 40 "baseline3.c" 1
	
	 movl    $222,%ebx #IACA/OSACA START MARKER
	 .byte   100,103,144     #IACA/OSACA START MARKER
# 0 "" 2
#NO_APP
	ret
	.cfi_endproc
.LFE28:
	.size	compute_tst, .-compute_tst
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
