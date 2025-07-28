$(function () {

  // jQuery selection for the 2 select boxes
  const dropdown = {
    county: $('#select_county'),
    county_mcma: $('#mass_cma_select_county'),
    town: $('#select_town'),
    village: $('#select_village'),
    village_mcma: $('#mass_cma_select_village'),
    assessment_mcma: $('#mass_cma_select_assessment'),
    sale_dates_from: $('#mass_cma_sale_dates_from'),
    sale_dates_to: $('#mass_cma_sale_dates_to')
  };
  let town = dropdown.town.val();
  town = town === '' ? '' : town;
  // call to update on load
  updateCounties(true);
  updateCounties();

  // function to call XHR and update county dropdown
  function updateCounties(isTown) {
    let send;
    dropdown.village.attr('disabled', 'disabled');
    dropdown.village_mcma.attr('disabled', 'disabled');
    if (dropdown.county.val() === 'nassau') {
      dropdown.village.removeAttr('disabled')
    }
    if (dropdown.county_mcma.val() === 'nassau') {
      dropdown.village_mcma.removeAttr('disabled')
    }
    if (isTown) {
      send = {
        county: dropdown.county.val()
      };
      dropdown.town.attr('disabled', 'disabled');
      dropdown.town.empty();
      $.getJSON("/rulesets/_get_counties", send, function (data) {
        data.forEach(function (item) {
          dropdown.town.append(
              $('<option>', {
                value: item[0],
                text: item[1]
              })
          );
        });
        dropdown.town.removeAttr('disabled');
        dropdown.town.val(town);
      });
    } else {
      send = {
        county: dropdown.county_mcma.val()
      };

      dropdown.assessment_mcma.attr('disabled', 'disabled');
      dropdown.assessment_mcma.empty();
      $.getJSON("/rulesets/_get_assessment", send, function (data) {
        data.forEach(function (item) {
          dropdown.assessment_mcma.append(
              $('<option>', {
                value: item[0],
                text: item[1]
              })
          );
        });
        dropdown.assessment_mcma.removeAttr('disabled');
        updateSaleDates();
      });

      let masscma_counties = ['nassau', 'suffolk'];
      if (!masscma_counties.includes(send.county)) {
        return
      }
      dropdown.village_mcma.attr('disabled', 'disabled');
      dropdown.village_mcma.empty();
      $.getJSON("/rulesets/_get_villages", send, function (data) {
        data.forEach(function (item) {
          dropdown.village_mcma.append(
              $('<option>', {
                value: item[0],
                text: item[1]
              })
          );
        });
        dropdown.village_mcma.removeAttr('disabled');
      });
    }
  }

  function updateSaleDates() {
    const assessment = {
      id: dropdown.assessment_mcma.val(),
      county: dropdown.county_mcma.val()
    };
    dropdown.sale_dates_from.attr('disabled', 'disabled');
    dropdown.sale_dates_from.empty();
    dropdown.sale_dates_to.attr('disabled', 'disabled');
    dropdown.sale_dates_to.empty();
    $.getJSON("/rulesets/_get_sale_dates", assessment, function (data) {
      dropdown.sale_dates_from.val(data.date_from);
      dropdown.sale_dates_to.val(data.date_to);
    });
    dropdown.sale_dates_from.removeAttr('disabled');
    dropdown.sale_dates_to.removeAttr('disabled');
  }

  // event listener to state dropdown change
  dropdown.county.on('change', function () {
    updateCounties(true);
  });

  dropdown.county_mcma.on('change', function () {
    updateCounties();
  });

  dropdown.assessment_mcma.on('change', function () {
    updateSaleDates();
  })

});

