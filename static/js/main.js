// Function to show loading screen
function showLoading() {
    document.getElementById("loadingOverlay").style.display = "flex";
}

function goBack() {
    // get the current URL
    const currentUrl = window.location.href;
    // trim the last part
    const trimmedUrl = currentUrl.replace(/\/[^\/]*\/?$/, '/');
    // go to the trimmed url
    window.location.href = trimmedUrl;
}