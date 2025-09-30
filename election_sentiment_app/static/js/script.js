// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.getElementById('file-name');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.color = '#2c3e50';
            } else {
                fileNameDisplay.textContent = 'No file selected';
                fileNameDisplay.style.color = '#777777';
            }
        });
    }
    
    // Accordion functionality
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    accordionItems.forEach(item => {
        const header = item.querySelector('.accordion-header');
        
        header.addEventListener('click', function() {
            // Close other open items
            accordionItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            item.classList.toggle('active');
        });
    });
    
    // Add active class to first accordion item by default
    if (accordionItems.length > 0) {
        accordionItems[0].classList.add('active');
    }
    
    // Animate stats on results page
    const animateStats = () => {
        const stats = document.querySelectorAll('.stat-value');
        
        stats.forEach(stat => {
            const value = parseFloat(stat.textContent);
            let startValue = 0;
            const duration = 1500;
            const increment = value / (duration / 16);
            
            const updateCounter = () => {
                if (startValue < value) {
                    startValue += increment;
                    stat.textContent = Math.min(startValue, value).toFixed(2) + '%';
                    requestAnimationFrame(updateCounter);
                } else {
                    stat.textContent = value.toFixed(2) + '%';
                }
            };
            
            requestAnimationFrame(updateCounter);
        });
    };
    
    // Check if we're on results page
    if (document.querySelector('.summary-stats')) {
        // Add animation after a slight delay
        setTimeout(animateStats, 300);
    }
});

// Form validation
const validateForm = () => {
    const fileInput = document.getElementById('file');
    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Please select a CSV file to upload');
        return false;
    }
    
    const fileName = fileInput.files[0].name;
    if (!fileName.toLowerCase().endsWith('.csv')) {
        alert('Please select a CSV file');
        return false;
    }
    
    return true;
};

// Add form validation to upload form
const uploadForm = document.querySelector('.upload-form');
if (uploadForm) {
    uploadForm.addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault();
        }
    });
}