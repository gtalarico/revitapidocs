$(".alert").delay(2500).fadeOut(500, function() {
    $(this).alert('close');
});

// activate popover
$("[data-toggle=popover]").popover();

$('#myTabs a[href="#profile"]').tab('show') // Select tab by name
$('#myTabs a:first').tab('show') // Select first tab
$('#myTabs a:last').tab('show') // Select last tab
$('#myTabs li:eq(2) a').tab('show') // Select third tab (0-indexed)