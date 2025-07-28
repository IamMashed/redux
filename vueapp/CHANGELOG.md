# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## YYYY-MM-DD - YYYY-MM-DD
### Added

### Changed

### Removed

### Fixed

## 2021-01-20 - 2021-02-26

### Added
- Added ability to send testing email template - **Email Template** - [link](https://app.asana.com/0/1147405519499344/1199952913347433/f)
- Added ability to save current template as json file - **Email Template** - [link](https://app.asana.com/0/1147405519499344/1199952913347433/f)
- Load starting template on email editor init - **Email Template** - [link](https://app.asana.com/0/1147405519499344/1199952913347433/f)
- Set default assessment date on county changes - **Make it possible for the user to select Assessment Set in the Search Page** - [link](https://app.asana.com/0/1147405519499344/1199410420174012/f)


## 2021-01-13 - 2021-02-19

### Added
- Added Email Template Page. Installed WYSIWYG email editor. Added ability to send testing email with generated HTML (WIP) - **Email Template** - [link](https://app.asana.com/0/1147405519499344/1199952913347433/f)
- Added Data Sets page with folder system loaded from server. Added ability to route between page with browser routing. Added breadcrumbs **Automated Data Sources - Front-end** - [link](https://app.asana.com/0/1147405519499344/1199937996192708/f)
- Don't select comps if FL and subject sale event - **Subject Sale - do not select other comps (FL Only)** - [link](https://app.asana.com/0/1147405519499344/1199935747180990/f)

### Fixed
- Added label to Assessment Field - **Make it possible for the user to select Assessment Set in the Search Page** - [link](https://app.asana.com/0/1147405519499344/1199410420174012/f)


## 2021-01-06 - 2021-02-12

### Added
- Make it possible for the user to select Assessment Set in the Search Page. Add `assessment date` query param for CMA page - **Make it possible for the user to select Assessment Set in the Search Page** - [link](https://app.asana.com/0/1147405519499344/1199410420174012/f)
- Added Extended Good/Bad report for Suffolk (WIP) - **Extended Good/Bad report for Suffolk only** - [link](https://app.asana.com/0/1147405519499344/1199620484266149/f)
- Add pagination to Advanced Search result (WIP) - **Advanced Search is not computationally optimized** - [link](https://app.asana.com/0/1147405519499344/1199207356750095/f)

## 2021-01-30 - 2021-02-05

### Added
- Add adjustment for Floor height - **Add adjustment for Floor height** - [link](https://app.asana.com/0/1147405519499344/1199564313516096/f)
- Add codes to location adj row - **Mapping Obsolescence list to "Simplified" dictionary** - [link](https://app.asana.com/0/1147405519499344/1199369947141702/f)

### Fixed
- Updated CMA Print PDF service to use table colspan. Updated pdfmake library to allow line truncating and prevent line break - **Prevent lines from going to the second line in the PDF Reports (CMA Report, Good/Bad report)** - [link](https://app.asana.com/0/1147405519499344/1199398959086141/f)
- Use `override_assessment_value` if exists - **Assessment Override needs to be applied everywhere** - [link](https://app.asana.com/0/1147405519499344/1199410420173992/f)
- Reload single cma when subject updated - **Adjusted Subject but recalculation did not happen** - [link](https://app.asana.com/0/1147405519499344/1199095280256448/f)

## 2021-01-23 - 2021-01-29

### Added
- Add adjustment for Floor height **(WIP)** - **Add adjustment for Floor height** - [link](https://app.asana.com/0/1147405519499344/1199564313516096/f)

### Fixed
- Resize map if map tab open to prevent map gets small issue - **Bug - Map gets small** - [link](https://app.asana.com/0/1147405519499344/1199608776940576/f)
- Updated CMA Print PDF service to use table colspan. Updated pdfmake library to allow line truncating and prevent line break **(WIP)** - **Prevent lines from going to the second line in the PDF Reports (CMA Report, Good/Bad report)** - [link](https://app.asana.com/0/1147405519499344/1199398959086141/f)

## 2021-01-16 - 2021-01-22

### Updated
- Refactor Map CLusterization. Create manual clusterization logic instead of Mapbox's clusterization that doesn't match client requirements. - **Issues with the pins on the map** - [link](https://app.asana.com/0/1147405519499344/1199704092118407/f)

### Fixed
- Don't close cluster unless user clicks on them - **Issues with the pins on the map** - [link](https://app.asana.com/0/1147405519499344/1199704092118407/f)
- Fixed automatic opening of cluster if they are not in viewport - **More issues with the cluster groups** - [link](https://app.asana.com/0/1147405519499344/1199706359409637/f)
- Open cluster with subject and selected comps when new property viewed (for example from result in quick search) - **More issues with the cluster groups** - [link](https://app.asana.com/0/1147405519499344/1199706359409637/f)
- Fix error on `npm install` - **npm install fails** - [link](https://app.asana.com/0/1147405519499344/1199646146833650/f)

## 2021-01-09 - 2021-01-15

### Fixed
- Pass all needed param to clusterization function to prevent issue with Print Map generation - **Cannot create CMA Workup** - [link](https://app.asana.com/0/1147405519499344/1199513679148629/f)

## 2021-01-01 - 2021-01-08

### Updated
- Moved pins on printed map closer to each other - **Print comps need to be closer to each other** - [link](https://app.asana.com/0/1147405519499344/1199706359409642/f)

### Fixed
- Fixed CMA Notification - **Why it does not mark the subj as a subject sale** - [link](https://app.asana.com/0/1147405519499344/1199407803991837/f)
- Update cluster layer and clear opened cluster on Subject id change - **Cluster Groups - conflicting data** - [link](https://app.asana.com/0/1147405519499344/1199709322591053/f)

## 2020-12-26 - 2020-12-31

### Updated
- Generate clustered coordinates for print map - **Single CMA Print - Map overlapping pins** - [link](https://app.asana.com/0/1147405519499344/1199648354353719/f)
- Increase font size of Good/Bad PDF report - **Issues in the Good/Bad report** - [link](https://app.asana.com/0/1147405519499344/1199410420174002/f)

## 2020-12-19 - 2020-12-25

### Added
- Clusterize comps on map if comps are in the same building - **Don't overlap If multiple comps are in the same building** - [link](https://app.asana.com/0/1147405519499344/1199337659065682/f)
- Randomize comps coordinates for print PDF report map if coords are the same  - **Don't overlap If multiple comps are in the same building** - [link](https://app.asana.com/0/1147405519499344/1199337659065682/f)
- Open cluster that contains selected comps - **Don't overlap If multiple comps are in the same building** - [link](https://app.asana.com/0/1147405519499344/1199337659065682/f)


## 2020-12-12 - 2020-12-18

### Added
- Add Market Value (Override) functionality - **Add Market Value (Override) functionality** - [link](https://app.asana.com/0/1147405519499344/1199398959088141/f)
- Pass assessment-date-id as param to CMA page - **Make it possible for the user to select Assessment Set in the Search Page** - [link](https://app.asana.com/0/1147405519499344/1199410420174012/f)

### Updated
- Set max zoom to 18 for printed map - **Map Zoom issue in evidence package** - [link](https://app.asana.com/0/1147405519499344/1199543385294184/f)
- Show condo info on 3 separate rows for broward - **Parse Broward condos extra info and display it on Single CMA as information** - [link](https://app.asana.com/0/1147405519499344/1199550998933701/f)
- Set `null` if market_value_override is empty - **Add Market Value (Override) functionality** - [link](https://app.asana.com/0/1147405519499344/1199398959088141/f)

### Fixed
- Fixed missing Comp model properties - **missing obsolescences on the map** - [link](https://app.asana.com/0/1147405519499344/1199608718699578/f)
- Fixed routing to approved and fully_rejected applications - **do not "404" approved applications url** - [link](https://app.asana.com/0/1147405519499344/1199608718699574/f)

### Removed
- Remove "Generate applicaton PDF" button - **Remove "Generate applicaton PDF" button** - [link](https://app.asana.com/0/1147405519499344/1199608718699583/f)


## 2020-12-05 - 2020-12-11

### Added
- Remove duplicate CMA obso polygons - **Restore transparency of obsolescences** - [link](https://app.asana.com/0/1147405519499344/1199543385294181/f)
- Reset text fields when new property loaded on CMA page - **Comments put into the comment box stay there when running another CMA on a different property** - [link](https://app.asana.com/0/1147405519499344/1199550998933712/f)
- Add condo view to bottom table header - **Add Condo View into bottom table possible filters** - [link](https://app.asana.com/0/1147405519499344/1199560234340133/f)
- Use current assessment as fallback for proposed assessment - **Proposed cannot be 40 for a property without comps** - [link](https://app.asana.com/0/1147405519499344/1199410420174017/f)
- Format GLA on CMA page and print report - **Gla is not formatted correctly.  Remove decimals, add commas.** - [link](https://app.asana.com/0/1147405519499344/1199410420173989/f)
- Show broward condo on CMA page - **Parse Broward condos extra info and display it on Single CMA as information** - [link](https://app.asana.com/0/1147405519499344/1199550998933701/f)


## 2020-11-28 - 2020-12-04

### Added
- Show "Re-run CMA with override assessment value" button on CMA page - **Single CMA Top-right table override column** - [link](https://app.asana.com/0/1147405519499344/1199333598401607/f)

### Fixed
- Fix proposed value for a property without comps - **Proposed cannot be 40 for a property without comps** - [link](https://app.asana.com/0/1147405519499344/1199410420174017/f)
- Highlight same street based on street - **Same Street sales should be highlighted in yellow.** - [link](https://app.asana.com/0/1147405519499344/1199410420173996/f)


## 2020-11-21 - 2020-11-27

### Added
- Stick header to top on cma page - **Make the top-right corner Single CMA table always visible (absolute position?)** - [link](https://app.asana.com/0/1147405519499344/1199333598401612/f)
- Use legal paper size for NY - **Single CMA Print and Good/Bad print** - [link](https://app.asana.com/0/1147405519499344/1199182161342673/f)
- Format class dispalay for nassau (3 digits) - **Single CMA Print and Good/Bad print** - [link](https://app.asana.com/0/1147405519499344/1199182161342673/f)
- Use maxHeight on table to prevent text wrap in Print Tables - **Single CMA Print and Good/Bad print** - [link](https://app.asana.com/0/1147405519499344/1199182161342673/f)
- Clasterize markers on map (WIP) - **Don't overlap If multiple comps are in the same building** - [link](https://app.asana.com/0/1147405519499344/1199337659065682/f)
 
### Updated
- Made obs-line features bolder - **Obsolescence shapes on the Single CMA Map need to display the obsolescence type** - [link](https://app.asana.com/0/1147405519499344/1199182161342693/f)
- Updated print pdf subheader - **Single CMA Print header** - [link](https://app.asana.com/0/1147405519499344/1199182161342681/f)

### Fixed
- Do not display null if no class desc is available - **Do not display null - just number for class if no translation is available** - [link](https://app.asana.com/0/1147405519499344/1199333598401615/f)
- Fixed Single CMA Print Max by law calculation - **Single CMA Print Max by law calculation** - [link](https://app.asana.com/0/1147405519499344/1199333598401609/f)
- Force to load counties list on cma search page - **Single CMA Search unselectable County** - [link](https://app.asana.com/0/1147405519499344/1199337659065675/f)
- Capitalize county name - **County starts with a capital letter** - [link](https://app.asana.com/0/1147405519499344/1199333598401619/f)



### 2020-11-14 - 2020-11-20

### Added
- Use legal paper size of CMA print report for non florida properties - **Single CMA Print for Nassau  & Suffolk Paper Size** - [link](https://app.asana.com/0/1147405519499344/1199182161342669/f)
- Show popup with obsolescence name on click on the map - **Obsolescence shapes on the Single CMA Map need to display the obsolescence type** - [link](https://app.asana.com/0/1147405519499344/1199182161342693/f)
- Show settlement in subheader for Nassau PDF CMA report - **Single CMA Print header** - [link](https://app.asana.com/0/1147405519499344/1199182161342681/f)

### Updated
- Disable fields in CMA search form if county is not selected - **Single CMA Search - grey out fields** - [link](https://app.asana.com/0/1147405519499344/1199182161337672/f)
- Make labels bigger on CMA search page - **Single CMA Search page** - [link](https://app.asana.com/0/1147405519499344/1199182161337669/f)
- Cover photo in PDF CMA report - **Subj photo is larger than comps in the Print Report** - [link](https://app.asana.com/0/1147405519499344/1199182161342676/f)

### Fixed
- Fixed loading userdata to prevent domain specific errors - **ptrc website: when user opens ptrcinternal.redux.tax** - [link](https://app.asana.com/0/1147405519499344/1198994208096751/f)
- Fixed CMA bottom table sorting in Google Chrome - **Single CMA - bottom table sorting does not work** - [link](https://app.asana.com/0/1147405519499344/1199232417395839/f)



## 2020-11-07 - 2020-11-13

### Added
- Added Hearing date column - **Advanced Search Results -> Cases** - [link](https://app.asana.com/0/1147405519499344/1198988436924578)
- Added workups column and ability to route directly to saved cma tabs on case page - **Advanced Search Results -> Cases** - [link](https://app.asana.com/0/1147405519499344/1198988436924578)
- Added unit field to cma search page - **Ongoing Single CMA Search issues** - [link](https://app.asana.com/0/1147405519499344/1199109153612257)
- Show ratio in cma settings dialog - **(NYC - Suffolk/Nassau) Need to show which ratio** - [link](https://app.asana.com/0/1147405519499344/1198994208096748)
- Enable/Disable Formatted rule value in the print report. - **Enable/Disable ($5/sf) etc in the print report.** - [link](https://app.asana.com/0/1147405519499344/1198994208096737)
- Show difference between override and proposed assessment - **Single CMA - Assessment Override is not working properly** - [link](https://app.asana.com/0/1147405519499344/1199109153612260/f)
- Format override assessment value input - **Single CMA - Assessment Override is not working properly** - [link](https://app.asana.com/0/1147405519499344/1199109153612260/f)
- Reload single cma when assessment updated - **Single CMA - Assessment Override is not working properly** - [link](https://app.asana.com/0/1147405519499344/1199109153612260/f)

### Updated
- Hide subdivision and land tag for not FL - **Land Tag and Subdivision should be removed for Nassau/Suffolk** - [link](https://app.asana.com/0/1147405519499344/1199172774391605/f)

## 2020-10-31 - 2020-11-06

### Added
- Add unselect all buttons - **Add "Unselect All" button at the single cma page.** - [link](https://app.asana.com/0/1147405519499344/1198977196885223)
- Add Export Lookup Results button - **Advanced Search Results export** - [link](https://app.asana.com/0/1147405519499344/1198988436924582)
- Display effective age in brackets - **Display Effective Age in brackets** - [link](https://app.asana.com/0/1147405519499344/1198994208096730)
- Reload cma page data on property id change - **Quick search bar malfunctions** - [link](https://app.asana.com/0/1147405519499344/1199089567892149)
- Show folio for FL in good/bad report table - **Florida Good/Bad Print** - [link](https://app.asana.com/0/1147405519499344/1199080734798577)
- Load CMA log separately on button click - **CMA Log change of the design to reduce loading time** - [link](https://app.asana.com/0/1147405519499344/1198984648998837)
- Use url hash routing for filter/results tabs on lookup page - **Advanced Search back button** - [link](https://app.asana.com/0/1147405519499344/1198988436924576)

### Fixed
- Fix Comps sorting - **Comps Sorting does not fully work** - [link](https://app.asana.com/0/1147405519499344/1198980098412687)
- Fix issue with twice cma search - **Single CMA Search issues** - [link](https://app.asana.com/0/1147405519499344/1198994208096735)
- Show pdf header from Misc Settings if not FL - **Use Legal Address from the Misc Settings for Nassau and Suffolk** - [link](https://app.asana.com/0/1147405519499344/1198994208096740)
- Fixed pdf header for non FL - **Use Legal Address from the Misc Settings for Nassau and Suffolk** - [link](https://app.asana.com/0/1147405519499344/1198994208096740)

### Updated
- Update cma-notification component - **Add Subject Disqualified Sale alert (similar to Subject Sale alert we have now)** - [link](https://app.asana.com/0/1147405519499344/1198948603327085)
- Update comps header - **Single CMA - Main Table - Comps Header (Digital version)** - [link](https://app.asana.com/0/1147405519499344/1198977196885225)
- Rename lookup filters - **Rename Filters** - [link](https://app.asana.com/0/1147405519499344/1198988436924573)
- Hide rule value for subject age adjustment - **Add Effective Age to the database** - [link](https://app.asana.com/0/1147405519499344/1198932172545944)
- Open cma as PTRC homepage - **ptrc website: when user opens ptrcinternal.redux.tax** - [link](https://app.asana.com/0/1147405519499344/1198994208096751)
- Improve readability improvement for CMA search page - **Readability improvement for Single CMA -> Search page** - [link](https://app.asana.com/0/1147405519499344/1199095280256441)


## 2020-10-24 - 2020-10-30

### Added
- Add Water Adjustment as an Adjustment - **Add Water Adjustment as an Adjustment** - [link](https://app.asana.com/0/1147405519499344/1198920864118085)
- Download petitions report - **Lookup -> Search -> Actions -> Excel Petitions Report** - [link](https://app.asana.com/0/1147405519499344/1198214050145175)
- Added Age adjustment to CMA page - **Add Age Adjustment** - [link](https://app.asana.com/0/1147405519499344/1198920864118092)
- Ignore good/bad sorting for florida at all - **Single CMA bottom table priority** - [link](https://app.asana.com/0/1147405519499344/1198950768791365)
- Do not open quick search item in new tab - **quick search bar - do not target="_blank"** - [link](https://app.asana.com/0/1147405519499344/1198977196885221)
- Search cma log by address - **CMA LOG - search by Address and Folio** - [link](https://app.asana.com/0/1147405519499344/1198214050145165)

### Removed
- Remove the "25%" for Florida **Remove the "25%" for Florida** - [link](https://app.asana.com/0/1147405519499344/1198899622600111)

### Fixed
- Use propper adj/v for florida in good/bad report - **Good/Bad report needs updating - the computation is not matching what Single CMA shows** - [link](https://app.asana.com/0/1147405519499344/1198962928276949)
- Optionally include Obsolescence into print pdf - **Cannot save workup when "Location" is ticked off from adjustments in Settings** - [link](https://app.asana.com/0/1147405519499344/1198976892151629)


## 2020-10-17 - 2020-10-23

### Added
- Subdivision column to bottom table on CMA page - **Improvements to the Single CMA - Comps Bottom Table** - [link](https://app.asana.com/0/1147405519499344/1198214727554218)
- Make bottom table settings icon visible again - **Improvements to the Single CMA - Comps Bottom Table** - [link](https://app.asana.com/0/1147405519499344/1198214727554218)
- Reset CMA'a bottom table columns to default - **Reset columns to default** - [link](https://app.asana.com/0/1147405519499344/1198557922723539)
- Ability to download good/bad report on saved cma's tab - **When user clicks "Save Workup" - it should save Good/Bad report too** - [link](https://app.asana.com/0/1147405519499344/1198187117566788)


## 2020-10-10 - 2020-10-16

### Added
- Show obs features on map - **Display Obsolescences on the map** - [link](https://app.asana.com/0/1147405519499344/1198003251410401)
- Link to Case Property from - **Add more clarity into activity log** - [link](https://app.asana.com/0/1147405519499344/1193253355179571)
- Show address on workup saved comment - **Missing Log of "Saved CMA"** - [link](https://app.asana.com/0/1147405519499344/1198214050145179)

### Updated
- Rename Lookup to Advanced Search - **rename "Lookup" to "Advanced Search"** - [link](https://app.asana.com/0/1147405519499344/1198214050145169)
- Open cases tab by default on lookup - **Lookup default to Cases (not Clients)** - [link](https://app.asana.com/0/1147405519499344/1198214050145173)

### Fixed
- Fixed buggy comps ordering. Use local copy of comps inside PDF service to prevent side effects and original data alteration - **Ordering Comps buggy** - [link](https://app.asana.com/0/1147405519499344/1198214050145177)
- Fixed hearing date filter - **Hearing Date search** - [link](https://app.asana.com/0/1147405519499344/1198214050145171)


## 2020-10-03 - 2020-10-09

### Added
- Save Workup's Proposed and Current value - **Need to save Workup's Proposed value** - [link](https://app.asana.com/0/1147405519499344/1197155661129145)
- Added evidence-package button to case - **Cover Page for the Evidence Package** - [link](https://app.asana.com/0/1147405519499344/1197029072487297)
- Added space around map markers - **Add a margin to the print map** - [link](https://app.asana.com/0/1147405519499344/1197405632574833)
- Download evidence package after workup creation - **Saving a Workup on the Single CMA page should automatically offer to save the Evidence Package** - [link](https://app.asana.com/0/1147405519499344/1197405632574836)
- Added case workup status and date filter to lookup page - **Lookup - Workup filters** - [link](https://app.asana.com/0/1147405519499344/1197314196783073)
- Include address_line_2 into pdf address row - **Print CMA - Address to include Unit** - [link](https://app.asana.com/0/1147405519499344/1197437347434865)
- Load workups by separate api call on Case Page - **Case/Client slow loading** - [link](https://app.asana.com/0/1147405519499344/1197405632574838)

### Updated
- Dynamically truncate cell content - **Obsolescence shouldn't wrap into 3rd line** - [link](https://app.asana.com/0/1147405519499344/1197683309773446)
- Change displayed adj_value for florida - **ADJ_VALUE needs to be COS Adjusted Sale $** - [link](https://app.asana.com/0/1147405519499344/1197683309773443)
- Show all comps on the map by default - **Default to "All Comps" on the map** - [link](https://app.asana.com/0/1147405519499344/1197437347434867)


## 2020-09-26 - 2020-10-03

### Added
- Show first 1-4 comps and ignore r_type for FL - **Florida single cma comps selection** - [link](https://app.asana.com/0/1147405519499344/1148093363185449)
- Added Class Code descriptions - **Class Code descriptions** - [link](https://app.asana.com/0/1147405519499344/1195920295858849)
- Added owners row to florida cma table - **Florida Single CMA changes** - [link](https://app.asana.com/0/1147405519499344/1195920295858842)
- Added "Gross Adjustments" to cma table - **Florida Single CMA changes** - [link](https://app.asana.com/0/1147405519499344/1195920295858842)
- Added subdivision to cma print report - **Subdivision** - [link](https://app.asana.com/0/1147405519499344/1195920295858851)
- Added Other Adjustment row - **Add: "Other Adjustment" at the end of adjustments as an extra row for manual entry** - [link](https://app.asana.com/0/1147405519499344/1168097257618577)
- Ability to download, set as primary and delete cma report for workup - **Complete workup process** - [link](https://app.asana.com/0/1147405519499344/1196804780578524)
- Added COS rows to Florida CMA Table - **Fix COS for FL** - [link](https://app.asana.com/0/1147405519499344/1196912201248274)

### Updated
- Show `C` flag for all comps on PDF report - **Fix print CMA report** - [link](https://app.asana.com/0/1147405519499344/1194804769595993)
- Shrink PDF header to fill table in one page - **Fix print CMA report** - [link](https://app.asana.com/0/1147405519499344/1194804769595993)
- Show Lot Size in Sqft - **LOT Square Feet** - [link](https://app.asana.com/0/1147405519499344/1195920295858847)
- Hide property photo row if there is no photo - **Single CMA Florida Print page re-shaping** - [link](https://app.asana.com/0/1147405519499344/1195875125344905)
- Set workup as primary on creation - **Complete workup process** - [link](https://app.asana.com/0/1147405519499344/1196804780578524)

### Removed
- Removed the "All Avg 1-4" from the single cma web - **Remove the "All Avg 1-4" from the single cma web** - [link](https://app.asana.com/0/1147405519499344/1195945545055017)
- Leave only one comment window for Florida - **Florida Single CMA changes** - [link](https://app.asana.com/0/1147405519499344/1195920295858842)
- Remove Buyer and Seller for FL - **Florida Single CMA changes** - [link](https://app.asana.com/0/1147405519499344/1195920295858842)


## 2020-09-19 - 2020-09-25

### Added
- Added ability to access "Applications' page when there are "0" applications - **Be able to access "Applications' page when there are "0" in the badge and the link is inactive** - [link](https://app.asana.com/0/1147405519499344/1194614805566177)
- Added Download DR486 Button to Case Page - **Add ability to Download DR486** - [link](https://app.asana.com/0/1147405519499344/1195068241682297)
- Added All Avg 1-4 and Good Avg 1-4 into the Single CMA Top Right corner **Add All Avg 1-4 and Good Avg 1-4 into the Single CMA Top Right corner** - [link](https://app.asana.com/0/1147405519499344/1195529955688651)

### Updated
- Rearrange menu - **Main Menu re-arranement** - [link](https://app.asana.com/0/1147405519499344/1195537357470962)

### Fixed
- Fixed case created at Lookup filter
- Fixed phone number field validation on copy/paste - **Copy/Paste phone number does not work** - [link](https://app.asana.com/0/1147405519499344/1194107564521313)
- Show bad comps on print map - **Fix print CMA report** - [link](https://app.asana.com/0/1147405519499344/1194804769595993)

## 2020-09-12 - 2020-09-18

### Added
- Export Lookup Cases results - **Export Lookup Cases results** - [link](https://app.asana.com/0/1147405519499344/1193253355179573)
- Ability to delete Client - **Client -> Actions -> Permanently Delete** - [link](https://app.asana.com/0/1147405519499344/1192987118852889)
- Ability to delete Сase - **Client -> Actions -> Permanently Delete** - [link](https://app.asana.com/0/1147405519499344/1192987118852889)
- Re-run lookup search when page was re-open - **Client -> Actions -> Permanently Delete** - [link](https://app.asana.com/0/1147405519499344/1192987118852889)
- Show fully rejected applications - **Add Fully Rejected tab to applications web page** - [link](https://app.asana.com/0/1147405519499344/1193355128006241)
- Added Case Country filter to Lookup page - **Lookup: Case County** - [link](https://app.asana.com/0/1147405519499344/1194107564515313)
- Added export of Lookup Case Folio TXT and Extended TXT report - **Export as TXT** - [link](https://app.asana.com/0/1147405519499344/1194107564517313)
- Show server error on Application creation fails - **When Creating an application and getting an error - display the error** - [link](https://app.asana.com/0/1147405519499344/1194140353281305)
- Add property type filter to lookup page - **Broward: split submission into vacant; residential; condo** - [link](https://app.asana.com/0/1147405519499344/1194417519720549)
- Added Improved Favicons - **Improvement to Favicon** - [link](https://app.asana.com/0/1147405519499344/1194558175244381)

### Fixed
- Show only countable application statuses in sidebar - **Do not count Fully Rejected into All Apps** - [link](https://app.asana.com/0/1147405519499344/1194244075376407)
- Fixed notification snackbar styles - **When Creating an application and getting an error - display the error** - [link](https://app.asana.com/0/1147405519499344/1194140353281305)


## 2020-09-05 - 2020-09-12

### Added
- Send status_id to filter applications - **Client -> Case ->"Applications" section is broken** - [link](https://app.asana.com/0/1147405519499344/1193138064382457)
- Client -> Actions -> Permanently Delete (WIP) - **Client -> Actions -> Permanently Delete** - [link](https://app.asana.com/0/1147405519499344/1192987118852889)

### Updated
- Add Lookup Cases Page (Finished) - **Lookup Cases (similar to clients)** - [link](https://app.asana.com/0/1147405519499344/1192141548076883)
- Load map for CMA PDF report from Mapbox Static API - **Use of static maps for the printing and back-end only code execution** - [link](https://app.asana.com/0/1147405519499344/1192466789756593)
- Update approved_contract icon - **Fix the duplicated "contract agreement sent" logs and a failure to download contracts** - [link](https://app.asana.com/0/1147405519499344/1192987118851894)

### Fixed
- Fixed infinity loader on cancel click - **Applications - Cancel button bug** - [link](https://app.asana.com/0/1147405519499344/1192356638655291)
- Unset user in at homepage redirect to allow normal data loading inside beforeEach route hook - **"0" applications and 404 error on refresh** - [link](https://app.asana.com/0/1147405519499344/1192987118852891)
- Dashboard 404 issue - **"0" applications and 404 error on refresh** - [link](https://app.asana.com/0/1147405519499344/1192987118852891)

-----------------------

## 2020-08-29 - 2020-09-05

### Added
- Add Lookup Cases Page (WIP) - **Lookup Cases (similar to clients)** - [link](https://app.asana.com/0/1147405519499344/1192141548076883)

### Fixed
- Allow to review physical applications without signature - **Allow review physical applications without signature** - [link](https://app.asana.com/0/1147405519499344/1191272390793337)
- Reload cma on settings changed - **(Bug) Switching Assessment Roll does not change the Assessed Value in the Single CMA** - [link](https://app.asana.com/0/1147405519499344/1184028802652401)
- Reinit autonumeric input on options change change to preevent some bugs - **Approved for Review tab counter and next button issues** - [link](https://app.asana.com/0/1147405519499344/1191882397130787)
- Wait for next application loading after review/approve/reject action. Prevent ability to manipulate with page until all data is loaded - **Switching Tabs on the Applications page does not always work well** - [link](https://app.asana.com/0/1147405519499344/1191165020441778)
- Fix homepage to application redirection for redux site - **Default Page for reduxinternal** - [link](https://app.asana.com/0/1147405519499344/1187279795623717)

-----------------------

## 2020-08-22 - 2020-08-28

### Added
- Add ability to create application - **A flow of creating the applications internally and sending a registration notice to the registered client** - [link](https://app.asana.com/0/1147405519499344/1189802505440801)
- Send sign email to client - **A flow of creating the applications internally and sending a registration notice to the registered client** - [link](https://app.asana.com/0/1147405519499344/1189802505440801)
- Disable "Review" and "Approve signature" buttons while there is no signature - **A flow of creating the applications internally and sending a registration notice to the registered client** - [link](https://app.asana.com/0/1147405519499344/1189802505440801)
- Added "Copy Payment Link" button to application and case pages - **Add Copy Payment Link** - [link](https://app.asana.com/0/1147405519499344/1189981801980793)
- Show condo_code and hide water_category for condos - **Condo View is not present** - [link](https://app.asana.com/0/1147405519499344/1190431985672580)
- Hide value column for florida - **Remove the "Value" column for the FL Counties** - [link](https://app.asana.com/0/1147405519499344/1190297828125273)
- Select pdf filename before print - **Be able to specify the file name of the "PDF"** - [link](https://app.asana.com/0/1147405519499344/1190297828126273)
- Ask to send new sign email - **A flow of creating the applications internally and sending a registration notice to the registered client** - [link](https://app.asana.com/0/1147405519499344/1189802505440801)

-----------------------

## 2020-08-15 - 2020-08-21

### Added
- highlight payment status in red if application is unpaid - **"unpaid" to be in red** - [link](https://app.asana.com/0/1147405519499344/1188616094092625)
- copy repair link to clipboard instead of opening - **"Copy Repair Link"** - [link](https://app.asana.com/0/1147405519499344/1188616094105625)
- "download" button on application tab in case page - **Case -> Applications Tab** - [link](https://app.asana.com/0/1147405519499344/1188208355572563)
- remember the county selection - **Remember the county selection** - [link](https://app.asana.com/0/1147405519499344/1183593714511343)
- prevent overscroll of comps table on cma page - **Single CMA Scrolling improvement** - [link](https://app.asana.com/0/1147405519499344/1183483869255674)
- show more descriptive info of invalid fields before application review/approve - **A warning message "fields do not match" needs to be more descriptive** - [link](https://app.asana.com/0/1147405519499344/1187814931191540)
- show apn and address at the top of the map - **Single CMA - Map Print** - [link](https://app.asana.com/0/1147405519499344/1182138881332400)
- Set the default page the Applications page if domain is `reduxinternal.redux.tax` - **Default Page for reduxinternal** - [link](https://app.asana.com/0/1147405519499344/1187279795623717)
- add daily emails field to shared settings - **Daily Emails** - [link](https://app.asana.com/0/1147405519499344/1189139258045929)
- show map parcels for non-nassau counties - **Parcels overlay is not working for non-Nassau counties** - [link](https://app.asana.com/0/1147405519499344/1189776260850209)

### Updated
- move client edit button to the right corner of the client info card - **Optimize the Client View Page space** - [link](https://app.asana.com/0/1147405519499344/1189139258045938)
- optimize the Client View Page space - **Optimize the Client View Page space** - [link](https://app.asana.com/0/1147405519499344/1189139258045938)

### Fixed
- automatically validate initial on first name/last name change - **Initials in the application verification issue** - [link](https://app.asana.com/0/1147405519499344/1187814931191537)
- fix map size on print on cma page - **Single CMA - Map Print** - [link](https://app.asana.com/0/1147405519499344/1182138881332400)
- fix county selection on rule set duplication - **Fix county selection on rule set duplication** - [link](https://app.asana.com/0/1147405519499344/1183980394870193)
- fix single cma proposed value 0 - **Single CMA Proposed value: 0** - [link](https://app.asana.com/0/1147405519499344/1184575061961371)
- repair the time format in the activity log - **Repair the time format in the activity log** - [link](https://app.asana.com/0/1147405519499344/1189756574985241)

-----------------------

## 2020-08-08 - 2020-08-14

### Added
- show warning alert if applicant is current client - **A banner text on the application page to notify if there is already a client with this email** - [link](https://app.asana.com/0/1147405519499344/1187814931191560)
- show page loader on application status change - **When user does an action to the final application in the queue it stays loaded and editable which needs changing** - [link](https://app.asana.com/0/1147405519499344/1187814931191563)
- redirect to another applications tab if no more in current queue - **When user does an action to the final application in the queue it stays loaded and editable which needs changing** - [link](https://app.asana.com/0/1147405519499344/1187814931191563)
- group search results by entity - **The Quick Search Bar results need to be groupped by categories to have a clearer picture of what user is clicking on** - [link](https://app.asana.com/0/1147405519499344/1188040167625091)
- PIN Code Entered to lookup filter - **Add pin_entered field to the application** - [link](https://app.asana.com/0/1147405519499344/1148093363185421)
- ask for Save Application changes before go to next/prev application - **If changes are made and user clicks on Next/Previous - the system should ask if they want to save or discard changes (instead of silently discarding)** - [link](https://app.asana.com/0/1147405519499344/1188241175822553)
- ability to edit Payment Type/Status of Case - **Being able to edit the payment type & status of the filing fee** - [link](https://app.asana.com/0/1147405519499344/1187135221358997)

### Updated
- logo size fo redux - **The logo needs to be changed** - [link](https://app.asana.com/0/1147405519499344/1188029128338985)
- do not highlight phone 2 field if it's empty - **Do not display a warning "!" for the phone 2 when it is empty** - [link](https://app.asana.com/0/1147405519499344/1187814931191555)
- rename column of lookup results - **Lookup Results rename created** - [link](https://app.asana.com/0/1147405519499344/1188241175822555)


### Fixed
- properly format phone number in client info section - **Phone number is incorrectly formatted on the Client Page** - [link](https://app.asana.com/0/1147405519499344/1187814931191546)
- input mask null value handle - **Phone 2 shows 0** - [link](https://app.asana.com/0/1147405519499344/1187814931191553)

-----------------------

## 2020-08-01 - 2020-08-07

### Added
- case payment status filter - **Migrate payment status, payment type from client to case property.** - [link](https://app.asana.com/0/1147405519499344/1186925178739393)
- case payment status on case page - **Migrate payment status, payment type from client to case property.** - [link](https://app.asana.com/0/1147405519499344/1186925178739393)
- add icons to each type of notes - **16. Icons in the Activity Log** - [link](https://app.asana.com/0/1147405519499344/1186530339195178)
- ability to edit Application only by Admin or Member - **Viewer Users** - [link](https://app.asana.com/0/1147405519499344/1186991248851922)
- open some pages for Viewer Role - **Viewer Users** - [link](https://app.asana.com/0/1147405519499344/1186991248851922)
- pin code to lookup filters - **6 character PIN Number changes** - [link](https://app.asana.com/0/1147405519499344/1185638973599396/f)
- pin code to case general-tab - **6 character PIN Number changes** - [link](https://app.asana.com/0/1147405519499344/1185638973599396/f)
- admin page with ability to view, create, update, delete userd - **Convert Admin Page to Vue** - [link](https://app.asana.com/0/1147405519499344/1179486293260985)
- add repair link to application info - **Application Repair Link** - [link](https://app.asana.com/0/1147405519499344/1186496164736045)
- view applications from the Case menu and allow to view approved/fully rejected applications - **View applications from the Case menu** - [link](https://app.asana.com/0/1147405519499344/1187135221358993)
- ability to send default Lookup filters - **Activity Log feedback 8/3/2020** - [link](https://app.asana.com/0/1147405519499344/1187279795623721)
- lookup only for current client by default - **Activity Log feedback 8/3/2020** - [link](https://app.asana.com/0/1147405519499344/1187279795623721)
- do not "squeeze" the User & Date columns if the message is long - **Activity Log should not "squeeze" the User & Date columns if the message is long** - [link](https://app.asana.com/0/1147405519499344/1187814931191557)
- use redux logo for redux site - **The logo needs to be changed** - [link](https://app.asana.com/0/1147405519499344/1188029128338985)

### Updated
- load attachemnt only on download icon click - **Clicking "Next"/"Previous" is too slow in the applications page** - [link](https://app.asana.com/0/1147405519499344/1187116111321990)
- limit quick-search results height - **Test Results / Bugs on Navigation bar  7/29/2020** - [link](https://app.asana.com/0/1147405519499344/1186761298601393)
- disable autocomplete for quick search form - **Test Results / Bugs on Navigation bar  7/29/2020** - [link](https://app.asana.com/0/1147405519499344/1186761298601393)
- fit layout to screen size on client page **15.	The Client Page should not have a scrollbar.** - [link](https://app.asana.com/0/1147405519499344/1186496164736057)
- rename Parcel # to Legal ID - **Test Results / Bugs on Application Page  7/29/2020** - [link](https://app.asana.com/0/1147405519499344/1186761298601400)
- rename "Show Property Info" to "Run Single CMA" - **In the General tab, “Show Property Info” is running a CMA on the property. That button should be renamed “Run Single CMA”** - [link](https://app.asana.com/0/1147405519499344/1187814931191549)

### Fixed
- hide link to application page if no application exists - **Significant issues with the Applications page** - [link](https://app.asana.com/0/1147405519499344/1187116111321987)
- optionally show tabs on application page if they contain applications - **Significant issues with the Applications page** - [link](https://app.asana.com/0/1147405519499344/1187116111321987)
- fix total application counter - **Significant issues with the Applications page** - [link](https://app.asana.com/0/1147405519499344/1187116111321987)
- fix Applications Counter - **Applications Counter is still wrong** - [link](https://app.asana.com/0/1147405519499344/1187914645441929)

-----------------------

## 2020-07-25 - 2020-07-31

### Added
- swap the red "!" and red background around - **Application Page feedback 07-14** - [link](https://app.asana.com/0/1147405519499344/1184575061961384)
- ask for approve on application review/approve - **Application Page feedback 07-14** - [link](https://app.asana.com/0/1147405519499344/1184575061961384)
- exact date selection to Case Create At field on Lookup page - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- ability to clear filters on Lookup page - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- ability to open client page directly - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- align lookup filters - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- billing filters to Lookup page - **Lookup Page** - [link](https://app.asana.com/0/1147405519499344/1182289859312321)
- reset comments form validation on blur - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- optional add payment amount input to application form - **Cash/Check payment type** - [link](https://app.asana.com/0/1147405519499344/1185638973599393)
- fix case client page to prevent undefined errors - **Test Results / Bugs on Applications / Case MAnagement 7/25/2020** - [link](https://app.asana.com/0/1147405519499344/1186130647641066)
- show error if email is failed - **Emails Table** - [link](https://app.asana.com/0/1147405519499344/1185841460958635/f)
- show error if signature is not approved - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- add link to lookup results page to allow native routing - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- ability to return to search results from client section - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- show loader on application loading to prevent accidentaly tabs change - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- update applications counter on application status change - **12.	The counters do not update when processing applications** - [link](https://app.asana.com/0/1147405519499344/1186496164736051)
- validate applications phone numbers - **11.	Display phone 1, phone 2 as "Red" if the number does not meet format. for example 1 missing digit** - [link](https://app.asana.com/0/1147405519499344/1186496164736049)
- ability to download files from activity log - **Activity logs must include records together with attachments from bounced emails and approved emails** - [link](https://app.asana.com/0/1147405519499344/1186469018058898)

### Fixed
- prevent underline being displayed incorrectly when loading - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- lookup, client pages appbar style - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- client's tags reset - **Test Results / Bugs on Applications / Case MAnagement 7/22/2020** - [link](https://app.asana.com/0/1147405519499344/1185811269382337)
- application layout - **Test Results / Bugs on Applications / Case MAnagement 7/25/2020** - [link](https://app.asana.com/0/1147405519499344/1186130647641066)

-----------------------

## 2020-07-18 - 2020-07-24

### Added
- ability to select multiple years for takeover application - **Back-end Applications Issues** - [link](https://app.asana.com/0/1147405519499344/1178714518567187)
- `application source`, `assigned_to`, `payment type`, `default fee percent`, `tax year`, `comment create/update by`, `comment created/updated at` filters to lookup page - **Lookup Page** - [link](https://app.asana.com/0/1147405519499344/1182289859312321)
- ability to allow mark filters as favorite - **Lookup Page** - [link](https://app.asana.com/0/1147405519499344/1182289859312321)
- not approved residential property alert - **Application Processing feedback 7-15** - [link](https://app.asana.com/0/1147405519499344/1184722810576660)
- link payment types to applicatio page - **Payment type not shown via pulbic api post** - [link](https://app.asana.com/0/inbox/1159959195971761/1185409557521585/1185424179331892)
- payment statuses select to application page - **Payment type not shown via pulbic api post** - [link](https://app.asana.com/0/inbox/1159959195971761/1185409557521585/1185424179331892)
- ability to move application to Approved for Review section - **Application Page feedback 07-14** - [link](https://app.asana.com/0/1147405519499344/1184575061961384)

### Updated
- rename Parcel # to "Legal ID" - **Application Processing feedback 7-15** - [link](https://app.asana.com/0/1147405519499344/1184722810576660)
- move tax year to the top line - **Application Page feedback 07-14** - [link](https://app.asana.com/0/1147405519499344/1184575061961384)

### Removed
- Dist/Sec/Block/Lot fields from application info - **Application Processing feedback 7-15** - [link](https://app.asana.com/0/1147405519499344/1184722810576660)

-----------------------

## 2020-07-11 - 2020-07-17

### Added
- ability to edit year of rule-set
- do not select bad comps by default. Only good comps
- application type to lookup filters
- case created filter at to lookup page
- release dates to assessment dates

### Update
- cma notification alert
- cma log wording

### Fixed
- add "," to the good / all average in the good/bad report
- yellow highlight for subject property

-----------------------

## 2020-07-04 - 2020-07-10

### Added
- `Added` and `Show Added` columns to CMA Log
- show plot buttons only if there are comps to show
- ability to submit filters on Enter ekypress on Lookup page
- auto switch to Results tab on Search on Lookup page
- case APN filter to Lookup page
- case Created by user filter to Lookup page
- show loader during lookup search
- ability to search passed comp in CMA Log, show `No Results` message
- obsolescence row to CMA compare table
- manual input in a-date component

### Updated
- rename `Apply Filters` button into `Search` on Lookup page
- rename `Case Tag` into `Client Tag`
- show `Actions` button only when Results visible on Lookup page
- cma notification alert (added statuses)

-----------------------

## 2020-06-27 - 2020-07-03

### Added
- water_category and land_tag to CMA table
- selection rules `same_building` and `prioritize_same_water_categories`
- added Lookup page - WIP
- added extended CMA log with ability to plot removed comps, search by apn

### Updated
- finished applications page (styles, layout)

-----------------------

## 2020-06-20 - 2020-06-26

### Added
- ability to highlight any cell on CMA comparison table and PDF print report
- navigate to rule set on table row click
- collapse the counties by default on tine adjs page
- cost of sale field to Rule Set
- show counties through out the website
- disable ability to change county when user are on the rulesets edit page
- do not allow to add empty messages to application activity

### Fixed
- print functionality (wait for map fully load)
- do not add tag to local list if it's not created
- allow only numeric values in ratios input

-----------------------

## 2020-05-13 - 2020-06-19

### Added
- properties photos on search result
- ability to clear towns select on rule sets page
- ability to show only selected comps on map
- updates to Assessment table on CMA page
- updates on how CMA recompute works

### Updated
- map pins
- print PDF report

### Removed
- Edit Mode button on CMA

-----------------------

## 2020-05-06 - 2020-06-12

### Added
- finished work on rule-set settings on CMA page
- dashboard page
- admin page (empty)
- hide pages and API calls based on current domain (for Redux site)
- ability to show tooltips with used rule_value on mouse hover on adjustments on CMA comparison table
- ability to show comps photos on Good/Bad PDF report
- disable Tags edition for non admin
- disable Application fully rejection for non admin
- disable Rule Set creation/edition/deletion for non admin
- disable Ratios edition for non admin
- disable Time Adjustments edition for non admin
- diasble Assessment dates edition/deletion for non admin
- disable Misc Settings edition for non admin
- disable CMA Override Database for non admin

### Updated
- marker colors on map

### Fixed
- issue with 210(0) class that cause crashing of CMA re-run
- bug "Dashboard tab in Navigation menu is always selected"

-----------------------

## 2020-05-30 - 2020-06-05

### Added
- show application count chip on sidebar menu and on tabs
- reset property search form
- allow fully reject application
- add CMA settings in popup. display current selection rules for CMA analysis

### Updated
- phone inputs on applications page
- takeover application (use client_id)
- allow change takeover year and client only for takeover application type
- style and numbers forma of CMA assessment table

-----------------------

## 2020-05-09 - 2020-05-15

### Added
- allow drag and drop photo handling
- allow copy and paste photo handling
- "Tags" page to create, edit and delete tags
- owner info to CMA search page
- ability to submit CMA searh form by Enter
- new look on application page (work in progress)

-----------------------

## 2020-05-02 - 2020-05-08

### Added
- list of applications
- allow to attach user to application
- allow to change list of clien/application tags
- allow to update application
- fly to comp on the map by clicking it on the comps table
- show red shade in main CMA table if comp status is "bad"
- ability to drag and drop photo

### Updated
- move, change and collapse cma filters icons on CMA page
- move comps table setting icon to header on CMA page

### Fixed
- map width on cma page tabs
- issue with empty selection rules on Rule Set Edit page

-----------------------

## 2020-04-25 - 2020-05-01

### Added
- ability to select assessment used for Single CMA + optiona Sale Date From/To params
- ability select columns showed on bottom comps table
- ability to rearrange columns in bottom comps table
- save bottom compsa table header configuration in localstorage

-----------------------

## 2020-04-18 - 2020-04-24

### Added
- "add" button on photo gallery slides
- nav buttons to thumbs gallery
- recalculate assesment result on frontend
- show YES/NO for boolean adjustments
- parcels toggle to show/hide tax layer on the map
- allow override property model on cma table dialog
- roads overlay on the map
- show buyer and seller on cma table

### Updated
- style of photo gallery (added border to active slide, removed opacity effect)
- normalizing photos size and width of CMA main table results
- tight photo gallery interface

### Fixed
- bottom table sort (make SBJ always be on the top)
- comparison table width (align the table to the left, not fullwidth)

-----------------------

## 2020-04-11 - 2020-04-17

### Added
- show cma alert if subject sale within date range, and arms length true, and if assessment value is lower than subject sale price
- photo gallery carousel
- ability to upload, update, select and delete photo in carousel gallery
- tax layer of Nassau to map

### Updated
- modify Nassau property class on front-end (remove last digit)

-----------------------

## 2020-04-04 - 2020-04-10

### Added
- best photo thumbnail on comps table
- show image tooltip on thumbnails hover
- ability to upload images for comps
- show placeholder when there is no photo for comp in comp selection table
- list of photos on comp's edit popup
- ability to delete images for comps
- ability to select photo as best for comp
- lock subject from dragging in comparison table

### Updated
- fields to use adjustments name instead keys

### Fixed
- lagging of the input box in single CMA. Caused by multiple emiting of `current-items` event of datatable, because of using spreading array as `items` props for data-table. Used computed property as prop instead.
- fix api interceptor to not null FormData

-----------------------

## 2020-03-28 - 2020-04-03

### Added
- titles to Good/Bad report's table
- beds to Good/Bad report tables
- results table to CMA pdf report
- split cma printable table into chunks per 6 comp
- apn on cma table
- print CMA pdf reporn on ctrl/cmd+P
- force county to be required for cma search
- add manual input fields for printable CMA report
- highlight showed row in comps table
- collapse cma map options

### Updated
- show apn on cma search results
- hide default footer for bottom cpm selection table
- fit cma map and comps table to screen size
- rebuild pdf generation of cma table
- print pdf filename
- sorting of comps in CMA table, save previous order after CMA re-run
- move property style from adjustments to configuration
- show "-" when no location on CMA table
- use last_sale_price/date
- rename bad comps to BC{n}

### Fix
- 25% max law rule
- sorting comps in bottom table
- display of location on CMA

-----------------------

## 2020-03-21 - 2020-03-27
### Added
- Show loading progress circle when searching properties for CMA
- Show nearby comps on pdf report
- Allow scroll bottom comp selection table
- Freeze SBJ row and headers in bottom comp selection table
- Show fake propety titles to CMA table
- Save selected comps on cma re-run
- Ability to select status of displayed comps on map
- Scroll to comp in the table on map property click event
- Search CMA visual re-arrangement + added APN as search param
- hide -25% law reduction row if curr assessed market below cut
- Rearrange top assessment_results table to reduce space
- Ability to rearrange comps on CMA table by dragging

### Updated
- Improvements to the Single CMA Print page
- Improved CMA page (updated data formats, text align)
- Comp selection table headers color
- Sidebars in vue and flask parts of the app
- Assessment Dates to use files as object

-----------------------

## 2020-03-14 - 2020-03-20
### Added
- ability to select properties on map
- ability to change map style
- map popup
- ability to get and update misc settings
- abuility to recalculate CMA after manual input

### Updated
- refactored CMA logic
- CMA print page
- Assessments table

-----------------------

## 2020-03-07 - 2020-03-13
### Added
- Constants API
- abuility to edit complex inventory rules values (like BASEMENT, HEAT_TYPE, PORCH_TYPE etc.)
- translation adjustments from code to string name on CMA page
- Misc Settings page
- make CMA page contenteditable
- map on CMA page with subject and good comps

### Updated
- reduced the space taken by CMA table
- to CMA page

-----------------------

## 2020-02-29 - 2020-03-06
### Added
- average_ranges to show on Single CMA PDF report
- ability to select comps for CMA analyze (bottom table)
- average_rabges to CMA PDF report
- translate Obsolescence from code to string name on CMA page

### Updated
- Single CMA PDF report
- install pdfmake from fork to fix columns sizes
- show only mentioned adjustment on PDF report

### Fixed
- small fixes for CMA page
- small fixes for Time Adjustments page

-----------------------

## 2020-02-22 - 2020-02-28
### Added
- Single CMA PDF report generation
- creation of Selection Rule if not exists
- Villages on Rule Set Edit page
- Adjustments api

### Updated
- display "settings" only for the Adjustments that are Enabled
- format of inventory rules inputs on Rule Set Edit page

### Fixed
- units, small bugs on Single CMA page
- units, small bugs on Rule Set Edit page
- issue when change id of Rule Set Edit page

-----------------------

## 2020-02-15 - 2020-02-21
### Added
- implementation of Single CMA API
- Selection, Inventory, Obsolescenses rules to Rule Set Edit page

### Updated
- some small things on Settings pages

-----------------------

## 2020-02-08 - 2020-02-14
### Added
- ability to select months ranges for grapsh on time adjustments page
- Single CMA search implementation
- Rule Sets CRUD table
- Rule Set creation page
- Rule Set edition page
- Single CMA compare page

### Changed

### Removed

### Fixed

-----------------------

## 2020-02-03 - 2020-02-07
### Added
- vue into flask integration
- Ratios page with edit functionality.
- Time Adjustments CRUD tables and graphs. Implemented Adjust to Date functionality.
- example of Single CMA page for properties search
- Assessment Dates CRUD table