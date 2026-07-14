

// var contractors = [
//   { name: "Agni Solutions Pvt Ltd", location: "Mumbai", service: "Fire Alarm", rating: 4.9, exp: 12, verified: true, tags: ["Alarm Systems", "Maintenance"], img: "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=250&fit=crop" },
//   { name: "SafeGuard Fire Systems", location: "Delhi", service: "Hydrant System", rating: 4.8, exp: 8, verified: true, tags: ["Industrial Hydrants", "NOC Help"], img: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=250&fit=crop" },
//   { name: "Elite Safety Hub", location: "Bangalore", service: "Fire Audit", rating: 5.0, exp: 15, verified: true, tags: ["Fire Audits", "Sprinklers"], img: "https://images.unsplash.com/photo-1536895058-45f7e6e2b4e0?w=400&h=250&fit=crop" },
//   { name: "Blaze Control India", location: "Mumbai", service: "Fire Extinguisher", rating: 4.7, exp: 10, verified: true, tags: ["Refilling", "Hydro-testing"], img: "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=400&h=250&fit=crop" },
//   { name: "Shield Fire Services", location: "Pune", service: "Sprinkler System", rating: 4.6, exp: 7, verified: true, tags: ["Residential", "Commercial"], img: "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=400&h=250&fit=crop" },
//   { name: "Safe Zone Engineers", location: "Delhi", service: "Fire Audit", rating: 4.5, exp: 6, verified: true, tags: ["Risk Assessment", "Compliance"], img: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=250&fit=crop" },
//   { name: "Reliable Fire Net", location: "Hyderabad", service: "NOC Assistance", rating: 4.8, exp: 9, verified: true, tags: ["NOC Docs", "Govt Liaison"], img: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=250&fit=crop" },
//   { name: "ProtectWell Solutions", location: "Chennai", service: "Fire Alarm", rating: 4.4, exp: 5, verified: true, tags: ["Detection", "Monitoring"], img: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=250&fit=crop" },
//   { name: "Rapid Fire Control", location: "Bangalore", service: "Fire Extinguisher", rating: 4.9, exp: 14, verified: false, tags: ["All Types", "Annual Check"], img: "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=400&h=250&fit=crop" },
//   { name: "SecurePoint Safety", location: "Kolkata", service: "Hydrant System", rating: 4.3, exp: 11, verified: true, tags: ["Pipeline", "Pump Room"], img: "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=400&h=250&fit=crop" },
//   { name: "Apex Fire Solutions", location: "Ahmedabad", service: "Maintenance", rating: 4.7, exp: 8, verified: true, tags: ["AMC", "24/7 Support"], img: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=250&fit=crop" },
//   { name: "Guardian Fire Care", location: "Pune", service: "NOC Assistance", rating: 4.6, exp: 6, verified: true, tags: ["Documentation", "Approvals"], img: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=250&fit=crop" },
//   { name: "Inferno Control Systems", location: "Hyderabad", service: "Sprinkler System", rating: 4.5, exp: 10, verified: true, tags: ["Design", "Installation"], img: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=250&fit=crop" },
//   { name: "Urban Fire Net", location: "Mumbai", service: "Maintenance", rating: 4.8, exp: 13, verified: true, tags: ["Preventive", "Emergency"], img: "https://images.unsplash.com/photo-1536895058-45f7e6e2b4e0?w=400&h=250&fit=crop" },
//   { name: "CertiFire India", location: "Delhi", service: "Fire Extinguisher", rating: 4.6, exp: 7, verified: true, tags: ["BIS Certified", "Refill"], img: "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=250&fit=crop" },
//   { name: "Suraksha Fire Systems", location: "Chennai", service: "Fire Audit", rating: 4.9, exp: 16, verified: true, tags: ["Detailed Audit", "NBC Compliance"], img: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&h=250&fit=crop" },
//   { name: "Nirmal Fire Safety", location: "Bangalore", service: "Hydrant System", rating: 4.4, exp: 5, verified: true, tags: ["Installation", "Testing"], img: "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=400&h=250&fit=crop" },
//   { name: "Pratham Fire Services", location: "Ahmedabad", service: "Fire Alarm", rating: 4.7, exp: 9, verified: false, tags: ["Smart Alarms", "Integration"], img: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=250&fit=crop" }
// ];

// var PER_PAGE = 6;
// var filteredList = [];
// var currentPage = 1;

// function buildCard(c) {
//   var stars = '';
//   var full = Math.floor(c.rating);
//   for (var i = 0; i < full; i++) stars += '<svg class="w-4 h-4 inline-block" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>';

//   var badge = c.verified
//     ? '<span class="inline-flex items-center gap-1 bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-medium"><svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>Verified</span>'
//     : '<span class="inline-flex items-center gap-1 bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full text-xs font-medium"><svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>Unverified</span>';

//   var tagsHtml = c.tags.map(function(t) {
//     return '<span class="bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full text-xs">' + t + '</span>';
//   }).join('');

//   return '<div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-md transition">' +
//     '<div class="h-36 overflow-hidden">' +
//       '<img src="' + c.img + '" alt="' + c.name + '" class="w-full h-full object-cover">' +
//     '</div>' +
//     '<div class="p-5">' +
//       '<div class="flex items-center justify-between mb-2">' +
//         '<span class="inline-block bg-[#A20513]/10 text-[#A20513] px-2 py-0.5 rounded-full text-xs font-medium">' + c.service + '</span>' +
//         badge +
//       '</div>' +
//       '<h3 class="text-lg font-bold text-gray-900">' + c.name + '</h3>' +
//       '<p class="text-sm text-gray-500 mt-1">' + c.location + ' &bull; ' + c.exp + ' yrs exp.</p>' +
//       '<div class="flex items-center gap-1 mt-2 text-yellow-500 text-sm font-medium">' +
//         stars + ' <span class="text-gray-600 ml-1">' + c.rating + '</span>' +
//       '</div>' +
//       '<div class="flex flex-wrap gap-2 mt-3">' + tagsHtml + '</div>' +
//     '</div>' +
//   '</div>';
// }

// function renderPagination() {
//   var el = document.getElementById('pagination');
//   var totalPages = Math.ceil(filteredList.length / PER_PAGE);
//   if (totalPages <= 1) { el.classList.add('hidden'); el.innerHTML = ''; return; }
//   el.classList.remove('hidden');

//   var html = '';

//   html += '<button onclick="goToPage(' + (currentPage - 1) + ')" ' + (currentPage === 1 ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg text-sm font-medium ' + (currentPage === 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-200') + '">Prev</button>';

//   for (var i = 1; i <= totalPages; i++) {
//     html += '<button onclick="goToPage(' + i + ')" class="w-9 h-9 rounded-lg text-sm font-medium ' + (i === currentPage ? 'bg-[#A20513] text-white' : 'text-gray-700 hover:bg-gray-200') + '">' + i + '</button>';
//   }

//   html += '<button onclick="goToPage(' + (currentPage + 1) + ')" ' + (currentPage === totalPages ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg text-sm font-medium ' + (currentPage === totalPages ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-200') + '">Next</button>';

//   el.innerHTML = html;
// }

// function goToPage(page) {
//   var totalPages = Math.ceil(filteredList.length / PER_PAGE);
//   if (page < 1 || page > totalPages) return;
//   currentPage = page;
//   renderCurrentPage();
// }

// function renderCurrentPage() {
//   var grid = document.getElementById('contractor-grid');
//   var noResults = document.getElementById('no-results');
//   var summary = document.getElementById('result-summary');

//   if (filteredList.length === 0) {
//     grid.innerHTML = '';
//     noResults.classList.remove('hidden');
//     document.getElementById('pagination').classList.add('hidden');
//     summary.textContent = 'Showing 0 - 0 of 0 verified businesses';
//     return;
//   }
//   noResults.classList.add('hidden');

//   var start = (currentPage - 1) * PER_PAGE;
//   var end = Math.min(start + PER_PAGE, filteredList.length);
//   var pageItems = filteredList.slice(start, end);
//   summary.textContent = 'Showing ' + (start + 1) + ' - ' + end + ' of ' + filteredList.length + ' verified businesses';

//   grid.innerHTML = pageItems.map(buildCard).join('');
//   renderPagination();
// }

// function filterContractors() {
//   var loc = document.getElementById('filter-location').value;
//   var svc = document.getElementById('filter-service').value;
//   var onlyVerified = document.getElementById('filter-verified').checked;
//   filteredList = contractors.filter(function(c) {
//     return (!loc || c.location === loc) && (!svc || c.service === svc) && (!onlyVerified || c.verified);
//   });
//   currentPage = 1;
//   renderCurrentPage();
// }

// function resetFilters() {
//   document.getElementById('filter-location').value = '';
//   document.getElementById('filter-service').value = '';
//   document.getElementById('filter-verified').checked = true;
//   filterContractors();
// }

// filterContractors();


function initSearchableDropdown(selectId, inputId, listId, emptyMessage) {
    const select = document.getElementById(selectId);
    const input = document.getElementById(inputId);
    const list = document.getElementById(listId);
    const dropdownId = inputId.replace('-input', '-dropdown');

    if (!select || !input || !list) return;

    const options = Array.from(select.options).slice(1);

    if (select.value) {
        input.value = select.options[select.selectedIndex].textContent;
    }

    function render(filter) {
        const q = (filter || '').toLowerCase().trim();
        let html = '';
        for (const opt of options) {
            const name = opt.textContent;
            if (!q || name.toLowerCase().includes(q)) {
                html += `<div class="px-4 py-2.5 cursor-pointer hover:bg-yellow-50 hover:text-yellow-700 text-sm" data-value="${opt.value}">${name}</div>`;
            }
        }
        if (!html) {
            html = `<div class="px-4 py-3 text-sm text-gray-400">${emptyMessage}</div>`;
        }
        list.innerHTML = html;
    }

    function selectItem(value, label) {
        select.value = value;
        input.value = label;
        list.classList.add('hidden');
    }

    input.addEventListener('focus', function() {
        render(input.value);
        list.classList.remove('hidden');
    });

    input.addEventListener('input', function() {
        if (!input.value.trim()) {
            select.value = '';
        }
        render(input.value);
        list.classList.remove('hidden');
    });

    list.addEventListener('click', function(e) {
        const item = e.target.closest('[data-value]');
        if (item) {
            selectItem(item.dataset.value, item.textContent);
        }
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('#' + dropdownId)) {
            list.classList.add('hidden');
        }
    });

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const first = list.querySelector('[data-value]');
            if (first) {
                e.preventDefault();
                selectItem(first.dataset.value, first.textContent);
            }
        }
        if (e.key === 'Escape') {
            list.classList.add('hidden');
        }
    });
}

initSearchableDropdown('location-select', 'location-input', 'location-list', 'No cities found');
initSearchableDropdown('rental_item-select', 'rental_item-input', 'rental_item-list', 'No categories found');