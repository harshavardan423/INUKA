
$('#map-image').maphilight();

document.addEventListener("DOMContentLoaded", function() {
    // Define the HTML content to be added
    var htmlContent = `
<img id="map-image" src="https://uploads-ssl.webflow.com/6602992da8068b9fa0c1b4ea/6614e90e30ab01e9c96d8931_world_map_9_2.png" usemap="#image-map">
    `;
    // Get the section element by its ID
    var section = document.getElementById("map-image-container");
    // Set the innerHTML of the section to the defined HTML content
    section.innerHTML = htmlContent;
    
    var customcontainer = document.getElementById("custom-container");
    var mapsectionhtml = `
    <map name=image-map><area alt=southafrica coords=306,1074,310,1083,319,1089,323,1085,332,1086,336,1082,350,1082,355,1084,359,1081,362,1082,365,1079,371,1079,381,1074,399,1056,408,1041,417,1035,420,1021,415,1022,414,1026,408,1026,402,1022,404,1013,411,1011,411,1001,407,990,407,983,395,983,390,986,385,988,379,993,377,993,375,999,370,1002,367,1006,364,1013,356,1014,345,1010,343,1011,341,1015,335,1022,331,1022,325,1022,322,1018,325,1014,321,1007,321,1035,316,1039,310,1040,301,1039,297,1035,294,1037,303,1057,308,1065,309,1070,306,1073 data-highlight-image=/static/images/southafrica2.jpg data-text="Kenya specific info"nohref shape=poly><area alt=kenya coords=469,838,458,831,459,826,429,811,430,801,437,795,439,786,437,781,434,778,434,776,431,771,438,764,442,765,442,770,448,771,458,775,463,778,473,778,476,775,481,773,484,775,487,775,483,780,482,810,486,816,481,822,478,822,471,837 data-highlight-image=/static/images/kenya3.jpg data-text="Kenya specific info"nohref shape=poly><area alt=france coords=153,438,158,442,167,443,172,442,176,444,180,446,184,446,187,447,187,440,197,436,205,438,212,440,222,433,216,428,216,423,215,420,218,417,216,408,210,409,221,395,226,380,199,371,183,357,178,356,175,358,175,365,174,367,165,373,165,375,155,374,151,372,149,373,151,378,151,383,146,383,134,382,127,385,129,391,137,393,147,398,151,408,157,417,152,435 data-highlight-image=/static/images/france.jpg data-text="Kenya specific info"nohref shape=poly target=""><area alt=oman coords=571,654,578,672,584,669,593,669,595,666,595,664,597,663,605,661,605,659,607,656,610,654,614,653,615,650,616,642,620,641,629,629,630,625,621,615,612,613,604,605,599,604,599,611,596,614,594,623,597,627,593,645,569,653 data-highlight-image=/static/images/muscat.jpg data-text="Kenya specific info"nohref shape=poly><area alt=egypt coords=360,548,360,626,447,626,441,623,439,613,427,586,423,582,424,578,415,566,415,559,419,559,430,576,435,563,429,551,413,551,409,547,400,549,392,554,368,548 data-highlight-image=/static/images/egypt.jpg data-text="Kenya specific info"nohref shape=poly></map>
    `;
    customcontainer.innerHTML = mapsectionhtml;
});