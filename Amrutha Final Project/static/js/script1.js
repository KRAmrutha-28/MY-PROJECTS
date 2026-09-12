fetch('/static/header.html')
    .then(Response => Response.text())
    .then(data => document.getElementById("header").innerHTML = data);

fetch('/static/footer.html')
    .then(Response => Response.text())
    .then(data => document.getElementById("footer").innerHTML = data);


function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// JavaScript to add interaction to the cards
document.getElementById('about-card').addEventListener('click', function() {
    alert('Learn more about our company and services in agriculture.');
  });
  
  document.getElementById('blogs-card').addEventListener('click', function() {
    alert('Explore our latest blogs on agriculture trends and tips.');
  });
  
  document.getElementById('fertilizers-card').addEventListener('click', function() {
    alert('Discover our range of fertilizers to boost crop growth.');
  });
  
  document.getElementById('contact-card').addEventListener('click', function() {
    alert('Get in touch with us through the contact form.');
  });
        // You can add additional interactive functionality here, for example, dynamically adding services or animations
        console.log("AgriTrade Website Loaded");  