// function to show loading screen
function showLoading() {
    document.getElementById("loadingOverlay").style.display = "flex";
}
// Function to go back to the previously visited page
function goBack() {
    showLoading();
    setTimeout(() => {
        document.getElementById("loadingOverlay").style.display = "none"; // Hide overlay
        window.history.back(); // Navigate back
    }, 100);
}