	.file	"test000.c"
	.text
	.p2align 4
	.globl	compute_model_tst
	.type	compute_model_tst, @function
compute_model_tst:
.LFB27:
	.cfi_startproc
	endbr64
	movl	(%rsi), %eax
	movl	4(%rsi), %esi
	vxorps	%xmm0, %xmm0, %xmm0
	movq	%rdi, %rcx
	movl	%eax, %edx
	imull	%esi, %edx
	addl	%edx, %edx
	addl	%edx, %eax
	vcvtsi2ssl	%edx, %xmm0, %xmm1
	addl	%esi, %eax
	cltq
	salq	$2, %rax
	js	.L2
	vcvtsi2ssq	%rax, %xmm0, %xmm0
	vunpcklps	%xmm0, %xmm1, %xmm1
	vmovlps	%xmm1, (%rcx)
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	shrq	%rax
	vcvtsi2ssq	%rax, %xmm0, %xmm0
	vaddss	%xmm0, %xmm0, %xmm0
	vunpcklps	%xmm0, %xmm1, %xmm1
	vmovlps	%xmm1, (%rcx)
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
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	movslq	(%rdi), %rdx
	movl	4(%rdi), %ebp
	movl	8(%rdi), %r10d
	movslq	12(%rdi), %rax
	movq	32(%rsi), %rbx
	movq	40(%rsi), %r9
	movq	16(%rcx), %rcx
	testl	%edx, %edx
	jle	.L15
	leaq	0(,%rax,4), %rsi
	movslq	%ebp, %rax
	leaq	(%rcx,%rdx,4), %r11
	xorl	%r8d, %r8d
	leaq	(%r9,%rax,4), %rdi
.L7:
	testl	%ebp, %ebp
	jle	.L17
	.p2align 4,,10
	.p2align 3
.L9:
	movslq	%r8d, %rax
	leaq	(%rbx,%rax,4), %rdx
	movq	%r9, %rax
	.p2align 4,,10
	.p2align 3
.L8:
#APP
# 38 "/home/hugoea/CCLabs/lab-2-taco/lab2_taco/lab_02_cc_taco_lab/CC_TACO_LAB/lab/objectives/objective-a/task-05/test000.c" 1
	
	 movl    $111,%ebx #IACA/OSACA START MARKER
	 .byte   100,103,144     #IACA/OSACA START MARKER
# 0 "" 2
#NO_APP
	vmovss	(%rdx), %xmm0
	vmulss	(%rax), %xmm0, %xmm0
	vaddss	(%rcx), %xmm0, %xmm0
	vmovss	%xmm0, (%rcx)
#APP
# 40 "/home/hugoea/CCLabs/lab-2-taco/lab2_taco/lab_02_cc_taco_lab/CC_TACO_LAB/lab/objectives/objective-a/task-05/test000.c" 1
	
	 movl    $222,%ebx #IACA/OSACA START MARKER
	 .byte   100,103,144     #IACA/OSACA START MARKER
# 0 "" 2
#NO_APP
	addq	$4, %rax
	addq	%rsi, %rdx
	cmpq	%rdi, %rax
	jne	.L8
	addq	$4, %rcx
	addl	%r10d, %r8d
	cmpq	%r11, %rcx
	jne	.L9
.L15:
	popq	%rbx
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L17:
	.cfi_restore_state
	addq	$4, %rcx
	addl	%r10d, %r8d
	cmpq	%r11, %rcx
	jne	.L7
	jmp	.L15
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
