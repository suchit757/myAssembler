section .data
	a dd 4
	b dd 5
	c dd 3
	sum dd 1,2,3,4
	msg db "Komal",10,0
section .bss
	n1 resd 1
	n2 resb 10
section .text
	global main
	extern printf,scanf
main:
	mov edx,ebx
	mov ebx,dword[ecx]
	mov ebx,dword[a]
	mov edx, dword[n2]
	mov ecx,1

	mov dword[c], edx
	mov dword[sum],'w'
	mov dword[ebx],10

