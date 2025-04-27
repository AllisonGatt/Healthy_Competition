
//ensures the DOM is fully loaded before running script
document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded"); //logging the loaded script

    //gets references to elements on the page based on the IDs
    const form = document.getElementById("activity-form");
    const successMessage = document.getElementById("success-message");
    const activityList = document.getElementById("activity-list"); // Dashboard <ul>
    const profileTable = document.getElementById("profile-activity-list"); // Profile table <tbody>

    if (!form) return; // Only runs if the form exists

    //event listener to handle submit event
    form.addEventListener("submit", function (e) {
        e.preventDefault(); //this prevents the default form submission so as to not reload the page

        console.log("Form submitted"); //logs the form has been submitted

        //creates formData object
        const formData = new FormData(form);

        fetch("/log-activity-ajax/", {
            method: "POST",
            headers: { //added CSRF token header for security 
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: formData, //sends the form data in the body of the request
        })
        .then((response) => response.json())//this waits for the server's respons and parses it as JSON
        .then((data) => {
            console.log("AJAX response:", data);//logs for debugging purposes

            //if sucess, proceed with updating the UI
            if (data.status === "success") {
                successMessage.style.display = "block"; //shows success message

                // Update dashboard activity list
                if (activityList) {
                    activityList.insertAdjacentHTML("afterbegin", data.row_html);
                }

                // Update profile activity table
                if (profileTable) {
                    profileTable.insertAdjacentHTML("afterbegin", data.profile_row_html);
                }
                //resets the form
                form.reset();
                //hides success message after 2 seconds
                setTimeout(() => {
                    successMessage.style.display = "none";
                }, 2000);
            } else {
                alert("Failed to log activity.");
            }
        })
        .catch((error) => console.error("Error:", error));
    });
});
