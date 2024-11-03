// Function to show loading screen
function showLoading() {
    document.getElementById("loadingOverlay").style.display = "flex";
}

function goBack() {
    // Redirect to the previous page and reload as a GET request
    // This ensures loading overlay do not stay.
    if (document.referrer) {
        window.location.href = document.referrer;
    } else {
        // Fallback if no referrer exists
        window.history.back();
    }
}