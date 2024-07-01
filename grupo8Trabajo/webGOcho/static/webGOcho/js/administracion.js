let btnEliminar = document.querySelectorAll('.btn-danger');
/*console.log(btnEliminar)*/

btnEliminar.forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault()
        alert('Usted está eliminando este elemento')
    })
})