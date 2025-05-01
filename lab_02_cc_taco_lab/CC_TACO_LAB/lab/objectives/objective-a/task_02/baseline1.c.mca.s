	.file	"baseline1.c"
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
	movq	%rcx, %rax
	movq	24(%rsi), %rdx
	movq	32(%rsi), %rcx
	movl	(%rdi), %edi
	movq	16(%rax), %rsi
#APP
# 32 "baseline1.c" 1
	# LLVM-MCA-BEGIN foo
# 0 "" 2
#NO_APP
	testl	%edi, %edi
	jle	.L6
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L7:
	vmovss	(%rdx,%rax,4), %xmm0
	vmulss	(%rcx,%rax,4), %xmm0, %xmm0
	vmovss	%xmm0, (%rsi,%rax,4)
	vmovss	4(%rdx,%rax,4), %xmm0
	vmulss	4(%rcx,%rax,4), %xmm0, %xmm0
	vmovss	%xmm0, 4(%rsi,%rax,4)
	addq	$2, %rax
	cmpl	%eax, %edi
	jg	.L7
.L6:
#APP
# 40 "baseline1.c" 1
	# LLVM-MCA-END
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
