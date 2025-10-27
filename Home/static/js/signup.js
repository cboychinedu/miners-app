// Greetings message 
console.log("This script was writted by Mbonu Chinedum"); 

// Getting the dom elements 
const email = document.getElementById("email"); 
const password = document.getElementById("password"); 
const confirmPassword = document.getElementById("confirmPassword"); 
const submitBtn = document.querySelector("#submitBtn"); 
const alertBox = document.querySelector("#alertBox");

// Adding event listener for the email address 
email.addEventListener("click", (event) => {
    alertBox.innerHTML = ""; 
    email.style.border = ""; 
})

// Adding event listener for the password 
password.addEventListener("click", (event) => {
    alertBox.innerHTML = ""; 
    password.style.border = ""; 
})

// Adding event listener for the confirm password 
confirmPassword.addEventListener("click", (event) => {
    alertBox.innerHTML = ""; 
    confirmPassword.style.border = ""; 
})

// Adding the event listener to the submit button 
submitBtn.addEventListener("click", (event) => {
    // Preventing default submission 
    event.preventDefault(); 

    // Checking the email address 
    if (!email.value) {
        // Setting the alert email address. 
        alertBox.innerHTML = "Email address is required!"; 
        email.style.border = "1px solid red"; 
    }

    // Checking the password if the user hasn't typed any 
    // value 
    else if (!password.value) {
        // Setting the alert box 
        alertBox.innerHTML = "Password is required!"; 
        password.style.border = "1px solid red"; 
    }

    // Checking the confirm password 
    else if (!confirmPassword.value) {
        // Setting the alert box 
        alertBox.innerHTML = "Confirm password is required!"; 
        confirmPassword.style.border = "1px solid red"; 
    }

    // Checking if the password and the confirm password is 
    // the same 
    else if(password.value !== confirmPassword.value) {
        // Checking 
        alertBox.innerHTML = "Passwords are not correct!";
        password.style.border = "1px solid red"; 
        confirmPassword.style.border = "1px solid red";  

    }

    // else if all the fields are correct get the data and send 
    // it to the backend 
    else {
        // Getting the user data 
        const userData = JSON.stringify({
            email: email.value, 
            password: password.value 
        })

        // Setting the server url 
        const serverUrl = "/signup";
    
        // Making a fetch request to the backend server 
        // Using try catch block 
        try {
            // Making a fetch request 
            fetch(serverUrl, {
                method: "POST", 
                headers: { "Content-Type": "application/json"},
                body: userData, 
            })
            // Handling the response from the server 
            .then((response) => response.json())
            .then((responseData) => {
                // Handle the response data on success 
                if (responseData.status === "success") {
                    // Redirect the user to the login page 
                    alertBox.style.color = "green"; 
                    alertBox.innerHTML = "User successfully registered!"; 

                    // Redirecting the user to the dashboard page, 
                    // and delay for 3 seconds  
                    setTimeout(() => {
                        window.location.href = "/dashboard"; 
                    }, 3000);  
                }

                // Else the status was not success 
                else {
                    // Execute the block of code below if the status 
                    // message was not successful 
                    alertBox.innerHTML = responseData.message; 
                    return; 
                }
            })
        }

        // Catch the error 
        catch (error) {
            // Logging the error 
            console.error("Error: ", error); 

            // Setting the error in the error message 
            alertBox.innerHTML = String(error); 
        }

    }

})