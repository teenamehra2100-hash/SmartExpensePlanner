
function showView(viewName) {
    // 1. Hide all views
    document.querySelectorAll('.view').forEach(function(view) {
        view.classList.remove('active');
    });
    // 2. Show the requested view
    document.getElementById('view-' + viewName).classList.add('active');
}

// Wait for the HTML to fully load before attaching click events
document.addEventListener("DOMContentLoaded", function() {
    
    // Attach click listener to the Dashboard button
    document.getElementById('nav-dashboard').addEventListener('click', function(e) {
        e.preventDefault(); // Stops the page from jumping to the top
        showView('dashboard');
    });

    // Attach click listener to the Transactions button
    document.getElementById('nav-transactions').addEventListener('click', function(e) {
        e.preventDefault();
        showView('transactions');
    });

    // Attach click listener to the Budgets button
    document.getElementById('nav-budgets').addEventListener('click', function(e) {
        e.preventDefault();
        showView('budgets');
    });

    // Attach click listener to the Add New button
    document.getElementById('nav-add').addEventListener('click', function(e) {
        e.preventDefault();
        showView('add');
    });

});