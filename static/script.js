document.addEventListener("DOMContentLoaded", function() {
    /*require at least one category be selected*/
    let form = document.getElementById("categories");
    let checkboxes = form.querySelectorAll("input[type='checkbox']");

    form.addEventListener("submit", function(event) {
        let is_checked = false;
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                is_checked = true;
            }
        });

        if (!is_checked) {
            event.preventDefault();
            alert("Please select at least one category");
        }
    });

    /*confirmation pop up*/
    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        const duplicate_form = new FormData(this);

        const response = await fetch("/", {
            method: "POST",
            body: duplicate_form
        });

        const result = await response.json();

        if (response.ok && result["success"]) {
            document.getElementById("successful_popup").style.display = "flex";
        }
        else {
            document.getElementById("failed_popup").style.display = "flex";
            document.getElementById("error_message").innerHTML = `${result["error_message"]} please try again`;
        }
    });
    /*close out the pop up*/
    document.getElementById("successful_ok").addEventListener("click", function() {
        document.getElementById("successful_popup").style.display = "None";
    });
    document.getElementById("failed_ok").addEventListener("click", function() {
        document.getElementById("failed_popup").style.display = "None";
    });
});
