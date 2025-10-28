// Greetings message 
console.log("This script was writted by Mbonu Chinedum"); 

// Getting the dom elements 
const email = document.querySelector("#email"); 
const password = document.querySelector("#password"); 
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

// Adding the event listener to the submit button 
submitBtn.addEventListener("click", (event) => {
    // Preventing default submission 
    event.preventDefault(); 

    // Checking the email address 
    if (!email.value) {
        // Setting the alert box 
        alertBox.innerHTML = "Email address is required!"; 
        email.style.border = "1px solid red"; 
    }

    // Else if the email address do not contain the 
    // @ symbol 
    else if (email.value.indexOf("@") === -1 ) {
        // Setting the alert dialog box 
        alertBox.innerHTML = "Email address is not complete!"; 
        email.style.border = "1px solid red"; 
    }

    // Checking the password if the user hasn't typed any 
    // value 
    else if (!password.value) {
        // Setting the alert box 
        alertBox.innerHTML = "Password is required!"; 
        password.style.border = "1px solid red"; 
    }

    // Else if all the field are correct get the data and 
    // send it to the backend 
    else {
        // Getting the user data 
        const userData = JSON.stringify({
            email: email.value, 
            password: password.value 
        }); 

        // Setting the server url 
        const serverUrl = "/login"; 

        // Making a fetch request to the backend server 
        // using try catch block to log the error's if any resulted 
        try {
            // Making a fetch request 
            fetch(serverUrl, {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json'}, 
                body: userData, 
                credentials: "include",
            })
            // Handling the response from the server 
            .then((response) => response.json())
            .then((responseData) => {
                // Handle the response data on success 
                if (responseData.status === "success") {
                    // Redirect the user to the dashboard page 
                    alertBox.style.color = "rgb(7 150 105)"; 
                    alertBox.innerHTML = "User logged in successfully!"; 

                    // Redirecting the user to the dashboard page, and delay for 3 seconds 
                    setTimeout(() => {
                        // Redirct the user after waiting for 4seconds  
                        window.location.href = "/dashboard"; 
                    }, 2000)
                }

                // Else if the status was not success execute this block 
                // of code below 
                else {
                    // Execute the block of code below 
                    alertBox.innerHTML = responseData.message
                    return; 
                }
                 
            })

        }

        // Catch the error 
        catch (error) {
            // Logging the error 
            console.error("Error: ", error); 

            // Showing the user the error message
            alertBox.innerHTML = String(error); 
        }
    }




})