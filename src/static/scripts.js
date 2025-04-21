document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded");

    const form = document.getElementById("activity-form");
    const successMessage = document.getElementById("success-message");
    const activityList = document.getElementById("activity-list"); // Dashboard <ul>
    const profileTable = document.getElementById("profile-activity-list"); // Profile table <tbody>

    if (!form) return; // Only run if the form exists

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        console.log("Form submitted");

        const formData = new FormData(form);

        fetch("/log-activity-ajax/", {
            method: "POST",
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("AJAX response:", data);

            if (data.status === "success") {
                successMessage.style.display = "block";

                // Update dashboard activity list
                if (activityList) {
                    activityList.insertAdjacentHTML("afterbegin", data.row_html);
                }

                // Update profile activity table
                if (profileTable) {
                    profileTable.insertAdjacentHTML("afterbegin", data.profile_row_html);
                }

                form.reset();

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
