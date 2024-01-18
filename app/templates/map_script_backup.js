<script>
    $(function () {
    $('#map-image').maphilight();

    // Variable to store default text
    var defaultText = "Hover over the area to see text.";
    var myDiv = document.getElementById('map-text-div');

    // Hover event for the image map area
    $('area').hover(
        function () {

            var content = getContent(this); // Get HTML content from a function, you can customize this function
            var highlightImage = $(this).data('highlight-image');
            var shapeAttribute = $(this).attr('shape');
            $('#map-text-div').css('display', ''); // Reset display property
            
            $('.custom-container2').css({
                'background-color': 'rgb(35, 35, 35)'
            });

            // Remove default text and update background color
            $('#map-text-div h3').fadeOut(300, function () {
                $(this).html('');
            });
            
            // Fade out the current background image
            $('#background-image').fadeOut(0, function () {
                // Set the new background image and fade it in
                $(this).css({
                    'background-color' : '#253336',
                    'background-image': 'url(' + highlightImage + ')',
                }).fadeIn(300);
            });

            // Set the new background image and fade it in
            $(this).css({
                'background-image': 'url(' + highlightImage + ')',
            }).fadeIn(500);

            // Fade out the current text content and update with the new content
            $('#text-div').fadeOut(300, function () {
                $(this).html(content).fadeIn(300);
            });

            // Check if the hovered area has shape 'circle'
            if (shapeAttribute === 'circle') {
                // Hide the circle
                $(this).hide();

                // Highlight the corresponding poly shape
                var correspondingPoly = getCorrespondingPoly(this);
                correspondingPoly.data('maphilight', {
                    'strokeColor': 'ffff00',
                    'strokeWidth': 0.1,
                    'fillColor': 'ffff00',
                    'fillOpacity': 0.1, // Set fillOpacity to 0 for full transparency
                    'alwaysOn': true
                }).trigger('alwaysOn.maphilight');
            }
            if (shapeAttribute === 'poly') {
                    // Existing code to handle circle areas
                    // Highlight the corresponding poly shape
                    var correspondingPoly = getCorrespondingPoly(this);
                    correspondingPoly.data('maphilight', {
                        'strokeColor': 'F8CB2E',
                        'strokeWidth': 0.1,
                        'fillColor': '000000',
                        'fillOpacity': 0,
                        'alwaysOn': false
                    }).trigger('alwaysOn.maphilight');
                } else if (shape !== 'poly') {
                   
                }
        },
        function () {
    // Reset content and fade out the current background image
    $('#background-image').fadeOut(300, function () {
        // Remove the background image
        $(this).css({
            'background-color': '#253336',
            'background-image': 'none',
        }).fadeIn(300);
    });

    // Reset background color of the custom-container
    $('.custom-container2').css({
        'background-color': 'transparent'
    });

    // Fade out the current text content and update with the default content
    $('#text-div').fadeOut(0, function () {
        $(this).html('<p></p>').fadeIn(100);
    });

    // Show the hidden circle when the mouse leaves the area
    $('area[shape="circle"]').show();

    // Remove highlighting from the corresponding poly shape
    $('area[shape="poly"]').data('maphilight', {}).trigger('alwaysOn.maphilight');

    $('#map-text-div').css('display', 'flex'); // Reset display property
    // Reset the default text content
    $('#map-text-div h3').fadeIn(400).html('Inuka has made impactful placements in emerging markets across the globe');
}

    );

    // Function to get HTML content based on the area
    function getContent(area) {
        switch ($(area).attr('alt')) {
    case 'kenya':
        return '<h2 style="color: #efd181; font-weight: 500">Kenya</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span>Development Director, East Africa</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Green Hydrogen Developer</p>' +  '<br>' +

            '<p><span style="color: #efd181;">Role : </span>Associate Investment Director</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund</p>' + '<br>' +


            '<p><span style="color: #efd181;">Role : </span>Chief Operating Officer</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Mini Grid Association</p>' + '<br>' +

            '<p><span style="color: #efd181;">Role : </span>Senior Associate</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund</p>' + '<br>' +
            
            '<p><span style="color: #efd181;">Role : </span>Senior Associate</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund</p>';


    case 'france':
        return '<h2 style="color: #efd181; font-weight: 500;">France</h2>' +
                '<p style="color: white;"><span style="color: #efd181;">Role :</span> Environmental & Social Manager</p>' +
                '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Developer</p>' ;

    case 'singapore':
        return '<h2 style="color: #efd181; font-weight: 500">Singapore</h2>' +
                '<p style="color: white; font-weight: bold;">Recent Placements</p>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span>Investment Manager</p>' +
            '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Fund</p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span>Project Finance Manager</p>' +
            '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Developer</p>';

    case 'southafrica':
        return '<h2 style="color: #efd181; font-weight: 500">South Africa</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span> Development Director, Southern Africa</p>' +
                '<p><span style="color: #efd181;">Company type :</span>Green Hydrogen Developer </p>' + '<br>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span> Head of Procurement</p>' +
                '<p><span style="color: #efd181;">Company type :</span>  Renewable Energy IPP </p>' + '<br>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span> Asset Director</p>' +
                '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund </p>' + '<br>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span>Non-Executive Director</p>' +
                '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Fund</p>' + '<br>' +

                '<p style="color: white;"><span style="color: #efd181;">Role :</span> Investment Associate</p>' +
                '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund </p>';

                

    case 'oman':
        return '<h2 style="color: #efd181; font-weight: 500">Oman</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Financial Analyst</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Global Energy Conglomerate</p>';

    case 'egypt':
        return '<h2 style="color: #efd181; font-weight: 500">Egypt</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            '<p style="color: white;"><span style="color: #efd181;">Role :</span>Business Development Manager</p>' +
            '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Developer </p>';

    case 'india':
        return '<h3 style="color: #efd181; font-weight: 500">India</h3>' +
        '<p style="color: white; font-weight: bold;">Recent Placements</p>' +

        '<p style="color: white;"><span style="color: #efd181;">Role :</span> Investment Associate </p>' +
        '<p><span style="color: #efd181;">Company type :</span> Investment Advisory Firm</p>';


    case 'nigeria':
        return '<h2 style="color: #efd181; font-weight: 500">Nigeria</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Business Operations Director </p>' +
            '<p><span style="color: #efd181;">Company type :</span> Energy Access Fund </p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Chief Executive Officer </p>' +
            '<p><span style="color: #efd181;">Company type :</span>Mini Grid Association </p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;"> Role :</span> Head of Digital Infrastructure </p>' +
            '<p><span style="color: #efd181;">Company type :</span> Private Equity Fund Portfolio Company</p>';
            

    case 'ivorycoast':
        return '<h2 style="color: #efd181; font-weight: 500">Ivory Coast</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Associate </p>' +
            '<p><span style="color: #efd181;">Company type :</span>  Financial Advisory Firm </p>';

    case 'morocco':
        return '<h2 style="color: #efd181; font-weight: 500">Morocco</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            '<p style="color: white;"><span style="color: #efd181;"> Role :</span>Senior Analyst</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Infrastructure Fund</p>';
            

    case 'england':
        return '<h2 style="color: #efd181; font-weight: 500">England</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            
            '<p style="color: white;"><span style="color: #efd181;">Role :</span>  Head of Energy Trading </p>' +
            '<p><span style="color: #efd181;">Company type :</span> Green Hydrogen Developer</p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Principal ESG Consultant </p>' +
            '<p><span style="color: #efd181;">Company type :</span> Investment Advisory Firm</p>' + '<br>' +


            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Senior BD Manager</p>' +
            '<p><span style="color: #efd181;">Company type :</span> Renewable Energy Developer</p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Consulting Manager, Climate Finance</p>' +
            '<p><span style="color: #efd181;">Company type :</span> Management Consulting Firm  </p>' + '<br>' +

            '<p style="color: white;"><span style="color: #efd181;">Role :</span>Engagement Manager, Climate Adaptation</p>' +
            '<p><span style="color: #efd181;">Company type :</span>  Management Consulting Firm</p>';

            

    case 'mauritius':
        return '<h2 style="color: #efd181; font-weight: 500">Mauritius</h2>' +
            '<p style="color: white; font-weight: bold;">Recent Placements</p>' +
            '<p style="color: white;"><span style="color: #efd181;">Role :</span> Financial Account</p>' +
            '<p><span style="color: #efd181;">Company type :</span>Renewable Energy Fund</p>';

    // Add more cases for other areas if needed

    default:
        return '<p>' + defaultText + '</p>';
}

    }

    // Function to get the corresponding poly area for a given circle area
    function getCorrespondingPoly(circleArea) {
        var correspondingPolyAlt = $(circleArea).attr('alt');
        return $('area[alt="' + correspondingPolyAlt + '"][shape="poly"]');
    }
});

</script>