const handleImageUpload = event => {
    const files = event.target.files
    console.log(files[0])
    const formData = new FormData()
    formData.append('myFile', files[0])

    fetch('/upload_user_avatar', {
        method: 'POST',
        body: formData,
    }).then(response => response.json()).then(data => {
        console.log(data.path)
    })
        .catch(error => {
            console.error(error)
        })
}

document.querySelector('.profile__avatar__change').addEventListener('change', event => {
    handleImageUpload(event)
})