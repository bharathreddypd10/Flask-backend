document.getElementById('search-input').addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const stations = document.querySelectorAll('#station-list li');

    stations.forEach(function(station) {
        const stationName = station.textContent.toLowerCase();
        if (stationName.includes(query)) {
            station.style.display = '';
        } else {
            station.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownBtn.addEventListener('click', function() {
        // Toggle the display of the dropdown menu
        if (dropdownContent.style.display === 'block') {
            dropdownContent.style.display = 'none';
        } else {
            dropdownContent.style.display = 'block';
        }
    });

    // Optional: Close the dropdown when clicking outside of it
    document.addEventListener('click', function(event) {
        if (!dropdownContent.contains(event.target) && !dropdownBtn.contains(event.target)) {
            dropdownContent.style.display = 'none';
        }
    });
});


