const usernameField = document.querySelector('#usernameField')
const feedbackArea = document.querySelector('.invalid-feedback')
const emailField = document.querySelector('#emailField')
const emailfeedbackArea = document.querySelector('.emailfeedbackArea')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')

const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent = 'HIDE'
        passwordField.setAttribute('type', 'text')
    }
    else{
        showPasswordToggle.textContent = 'SHOW'
        passwordField.setAttribute('type', 'password')
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)

emailField.addEventListener('keyup', (e)=> {
    emailField.classList.remove('is-invalid')
    emailfeedbackArea.style.display = "none"
    const emailVal = e.target.value
    if (emailVal.length > 0) {
        fetch('/authentication/validate-email',
            {
                body: JSON.stringify({'email': emailVal}),
                method: 'POST',
            }
        ).then(res=> res.json()).then(data => {
            if (data.email_error){
                submitBtn.disabled = true
                emailField.classList.add('is-invalid')
                emailfeedbackArea.style.display = 'block'
                emailfeedbackArea.innerHTML= `<p>${data.email_error}</p>`
            }
            else{
                submitBtn.disabled = false
            }
        })
    }
})


usernameField.addEventListener('keyup', (e) => {
    usernameField.classList.remove('is-invalid')
    feedbackArea.style.display = "none"
    const usernameVal = e.target.value
    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username',
            {
                body: JSON.stringify({'username': usernameVal}),
                method: 'POST',
            }
        ).then(res=> res.json()).then(data => {
            if (data.username_error){
                submitBtn.disabled = true
                usernameField.classList.add('is-invalid')
                feedbackArea.style.display = 'block'
                feedbackArea.innerHTML= `<p>${data.username_error}</p>`
            }
            else{
                submitBtn.disabled = false
            }
        })
    }
})