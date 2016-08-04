import os
import re

print(os.getcwd())
DIR = '../app/templates/2015/'
# TEST = '../app/templates/2015/z.htm'

CSS_MACRO = "{% assets \"css_chm\" %}<link rel=\"stylesheet\" type=\"text/css\" href=\"{{ ASSET_URL }}\" />{% endassets %}"
JS_MACRO = "{% assets \"js_assets\" %}<script src=\"{{ ASSET_URL }}\"></script>{% endassets %}"
ASSETS_MACRO = CSS_MACRO + JS_MACRO

''' This script makes the replacements below, and ensures all patterns are
substituted, no more, no less than 1 time, otherwise raises exception'''
replacements = (
               (r'<html.+\<head>', r"{% macro header() %}"),
               (r'<META HTTP-EQUIV.+?history" />', ''),
               (r'<meta name="Lan.+?erence" />', ''),
               (r'<xml>.+?</xml>', ''),
               (r'</head>.*?<body>', r'{% endmacro %}'),
               (r'<input type="hidden" id="userDataCache.*over image" />', ''),
               (r'<table id="gradi.+?</table>', ''),
               (r'<table id="topTa.*?</table>', ''),
               (r'<div id="devl.*?</div>', ''),
               (r'<div id="allHistory.*?DarkGray"></span>', ''),
               (r'<div id="footer.*script>.*?</div>', ''),
               (r'<link.*?CommonUtilities.*?</script>', ASSETS_MACRO),
               (r'</body.+?html>', ''), )

for f in sorted(os.listdir(DIR))[:]:
    with open(DIR+f, 'r') as fp:
    # with open(TEST, 'r') as fp:
        new_text = fp.read()
    print('FILE:', fp)
    results = []
    for pat, replacement in replacements:
        new_text, subs = re.subn(pat, replacement, new_text, flags=re.DOTALL)
        results.append(subs)

    # print('RESULTS:', results)
    all_ones = [r == 1 for r in results]
    if not all(all_ones):
        raise Exception('Not all ones')
    # print(new_text)
    # with open('../app/templates/2015/z2.htm', 'w') as fp:
        # fp.write(new_text)
print('success')
# print(text)
# print('-'*50)
# print(new_text)
# for filename in os.listdir(DIR)[0:3]:


# DELETE
# <table id="gradientTable">
#     <tr>
#         <td class="nsrBottom" background="../icons/gradient.gif" />
#     </tr>
# </table>

# DELETE
# <div id="footer">
#     <div class="footerLine"><img width="100%" height="3px" src="../icons/footer.gif" alt="Footer image" title="Footer image" /></div>
#     <A NAME="feedback"></A><span id="fb" class="feedbackcss"></span>
#     <p />Send comments on this topic to
#     <a id="HT_MailLink" href="mailto:revitapifeedback%40autodesk.com?Subject=Revit 2015 API">Autodesk</a>
#     <script type="text/javascript">
#         var HT_mailLink = document.getElementById("HT_MailLink");
#         var HT_mailLinkText = HT_mailLink.innerHTML;
#         HT_mailLink.href += ": " + document.title;
#         HT_mailLink.innerHTML = HT_mailLinkText;
#     </script>
# </div>

# DELETE
# <table id="topTable" cellspacing="0" cellpadding="0">
#     <tr>
#         <td><span onclick="ExpandCollapseAll(toggleAllImage)" style="cursor:default;" onkeypress="ExpandCollapseAll_CheckKey(toggleAllImage, event)" tabindex="0"><img ID="toggleAllImage" class="toggleAll" src="../icons/collapse_all.gif" /> <label id="collapseAllLabel" for="toggleAllImage" style="display: none;">Collapse All</label><label id="expandAllLabel" for="toggleAllImage" style="display: none;">Expand All</label> </span><span>    </span>
#             <span
#                 id="devlangsDropdown" class="filter" tabindex="0"><img id="devlangsDropdownImage" src="../icons/dropdown.gif" />
#                 <label id="devlangsMenuAllLabel" for="devlangsDropdownImage" style="display: none;">
#                     <nobr>Code: All </nobr>
#                 </label>
#                 <label id="devlangsMenuMultipleLabel" for="devlangsDropdownImage" style="display: none;">
#                     <nobr>Code: Multiple </nobr>
#                 </label>
#                 <label id="devlangsMenuCSharpLabel" for="devlangsDropdownImage" style="display: none;">
#                     <nobr>Code: C# </nobr>
#                 </label>
#                 <label id="devlangsMenuVisualBasicLabel" for="devlangsDropdownImage" style="display: none;">
#                     <nobr>Code: Visual Basic </nobr>
#                 </label>
#                 <label id="devlangsMenuManagedCPlusPlusLabel" for="devlangsDropdownImage" style="display: none;">
#                     <nobr>Code: Visual C++ </nobr>
#                 </label>
#                 </span>
#         </td>
#     </tr>
# </table>
