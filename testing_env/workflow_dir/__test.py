#!/usr/bin/python
# encoding: utf-8
from __future__ import unicode_literals

import sys
import unittest
import subprocess
from collections import OrderedDict

import utils
from workflow import Workflow
from lib import xmltodict

## -----------------------------------------------------------------------------

EXPECTED_MD_COLL = "Cicero, Marcus Tullius. 2001. _Cicero: On Moral Ends_. Edited by Julia Annas. Translated by Raphael Woolf. Cambridge University Press.\n\nDe Lacy, Phillip. 1957. \u201cProcess and Value: An Epicurean Dilemma.\u201d In _Transactions and Proceedings of the American Philological Association_, 88:114\u201326. http://www.jstor.org/stable/10.2307/283897.\n\nDe Lacy, Phillip Howard. 1948. \u201cLucretius and the History of Epicureanism.\u201d In _Transactions and Proceedings of the American Philological Association_, 12\u201323. http://www.jstor.org/stable/10.2307/283350.\n\nAnnas, Julia. 1995. _The Morality of Happiness_. Oxford University Press, USA. http://books.google.com/books?hl=en&lr=&id=KRfwSjk3fBcC&oi=fnd&pg=PA3&dq=Annas,+The+Morality++of+Happines&ots=MWfobwkmG7&sig=yD2gl9SInY-Ssq2xaos3G2g6XUs.\n\nCooper, John M. 1995. \u201cEudaimonism and the Appeal to Nature in the Morality of Happiness: Comments on Julia Annas, The Morality of Happiness.\u201d _Philosophy and Phenomenological Research_ 55 (3): 587\u201398. http://www.jstor.org/stable/10.2307/2108440.\n\nAnnas, Julia. 2011. \u201cEpicurean Emotions.\u201d _Greek, Roman, and Byzantine Studies_ 30 (2): 145\u201364. http://grbs.library.duke.edu/article/view/4261/0.\n\nDiels, Hermann. 1917. \u201cPhilodemos \xdcber Die G\xf6tter: Drittes Buch (commentary).\u201d _Abhandlungen Der Koniglich Preussischen Akademie Der Wissenschaften_ 6.\n\nDiels, Hermann. 1917. \u201cPhilodemos \xdcber Die G\xf6tter: Drittes Buch (text).\u201d _Abhandlungen Der Koniglich Preussischen Akademie Der Wissenschaften_ 4.\n\nArrighetti, Graziano. 1961. \u201cFilodemo, De dis III, col. XII - XIII,20.\u201d _Studi classici e orientali_ 10: 112\u201321.\n\nArrighetti, Graziano. 1958. \u201cFilodemo, De dis III, col. X - XI.\u201d _Studi classici e orientali_ 7: 83\u201399.\n\nClay, Diskin. 1998. \u201cIndividual and Community in the First Generation of the Epicurean School.\u201d In _Paradosis & Survival: Three Chapters in the History of Epicurean Philosophy_, 55\u201374. Ann: University of Michigan Press.\n\nClay, Diskin. 1998. _Paradosis & Survival: Three Chapters in the History of Epicurean Philosophy_. University of Michigan Press. http://www.google.com/books?hl=en&lr=&id=qXRoD9bYe90C&oi=fnd&pg=PR17&dq=Paradosis+and+Survival&ots=LOu4DJboKb&sig=nYcJg5TtaOm0_SWOp1IpBtCxnI0.\n\nArmstrong, David. 2011. \u201cEpicurean Virtues, Epicurean Friendship: Cicero vs the Herculaneum Papyri.\u201d In _Epicurus and the Epicurean Tradition_, edited by Jeffrey Fish and Kirk R. Sanders, 105\u201328. Cambridge: Cambridge University Press.\n\nFish, Jeffrey, and Kirk R. Sanders, eds. 2011. _Epicurus and the Epicurean Tradition_. Cambridge University Press.\n\nEvans, Matthew. 2004. \u201cCan Epicureans Be Friends?\u201d _Ancient Philosophy_ 24 (2): 407\u201324. http://www.philosophie.uni-muenchen.de/lehreinheiten/philosophie_3/personen/hasper/verg_sem/lv_sose_2011/freundschaft/evans_epicur_freund.pdf.\n\nStern-Gillet, Suzanne. 1989. \u201cEpicurus and Friendship.\u201d _Dialogue: Canadian Philosophical Review/Revue Canadienne de Philosophie_ 28 (02): 275\u201388. doi:10.1017/S0012217300015778.\n\nWheeler, M. R. 2003. \u201cEpicurus on Friendship: The Emergence of Blessedness.\u201d In _Epicurus: His Continuing Influence and Contemporary Relevance_, edited by Dane R. Gordon and David B. Suits, 183\u201394. RIT Cary Graphic Arts Press.\n\nGordon, Dane R., and David B. Suits, eds. 2003. _Epicurus: His Continuing Influence and Contemporary Relevance_. RIT Cary Graphic Arts Press.\n\nMitsis, Phillip. 1989. _Epicurus' Ethical Theory: The Pleasures of Invulnerability_. Cornell University Press. http://www.amazon.ca/exec/obidos/redirect?tag=citeulike09-20&path=ASIN/080142187X.\n\nGiannantoni, Gabriele, Marcello Gigante, and Francesca Alesse. 1996. _Epicureismo Greco E Romano: Atti Del Congresso Internazionale: Napoli, 19-26\xa0Maggio 1993 / a Cura Di Gabriele Giannantoni E Marcello Gigante_. Napoli: Bibliopolis.\n\nKonstan, David. 1996. \u201cFriendship from Epicurus to Philodemus.\u201d In _Epicureismo Greco E Romano_. Bibliopolis.\n\nThibodeau, Philip. 2003. \u201cCan Vergil Cry? Epicureanism in Horace Odes 1.24.\u201d _The Classical Journal_ 98 (3): 243\u2013256. http://www.jstor.org/stable/3298047.\n\nSnyder, Jane McIntosh. 1973. \u201cThe Poetry of Philodemus the Epicurean.\u201d _The Classical Journal_ 68 (4): 346\u2013353. http://www.jstor.org/stable/3295958.\n\nDeWitt, Norman W. 1937. \u201cThe Epicurean Doctrine of Gratitude.\u201d _The American Journal of Philology_ 58 (3): 320\u2013328. http://www.jstor.org/stable/290330.\n\nDeWitt, Norman W. 1936. \u201cEpicurean Contubernium.\u201d _Transactions and Proceedings of the American Philological Association_ 67: 55\u201363. http://www.jstor.org/stable/283227.\n\nArmstrong, John M. 1997. \u201cEpicurean Justice.\u201d _Phronesis_ 42 (3): 324\u2013334. http://www.jstor.org/stable/4182567.\n\nKeith, Arthur L. 1929. \u201cCicero's Idea of Friendship.\u201d _The Sewanee Review_ 37 (1): 51\u201358. http://www.jstor.org/stable/27534355.\n\nFarrington, B. 1954. \u201cLucretius and Manilius on Friendship.\u201d _Hermathena_, no. 83: 10\u201316. http://www.jstor.org/stable/23039315.\n\nBrown, Eric. 2002. \u201cEpicurus on the Value of Friendship (\u2018Sententia Vaticana' 23).\u201d _Classical Philology_ 97 (1): 68\u201380. http://www.jstor.org/stable/1215547.\n\nRist, John M. 1980. \u201cEpicurus on Friendship.\u201d _Classical Philology_ 75 (2): 121\u2013129. http://www.jstor.org/stable/268919.\n\nAllen, Walter, Jr. 1938. \u201cOn the Friendship of Lucretius with Memmius.\u201d _Classical Philology_ 33 (2): 167\u2013181. http://www.jstor.org/stable/263976.\n\nHall, Clayton M. 1935. \u201cSome Epicureans at Rome.\u201d _The Classical Weekly_ 28 (15): 113\u2013115. http://www.jstor.org/stable/4339501.\n\nPorter, James I. 2003. \u201cEpicurean Attachments: Life, Pleasure, Beauty, Friendship, and Piety.\u201d _Cronache Ercolanesi_ 2003 (33): 205\u201323.\n\nO'Connor, David K. 2011. \u201cThe Invulnerable Pleasures of Epicurean Friendship.\u201d _Greek, Roman, and Byzantine Studies_ 30 (2): 165\u201386. https://openpublishing.library.duke.edu/index.php/grbs/article/viewArticle/4271.\n\nTurner, J. Hilton. 1947. \u201cEpicurus and Friendship.\u201d _The Classical Journal_ 42 (6): 351\u201356. http://www.jstor.org/stable/10.2307/3291646.\n\nO'Keefe, Tim. 2001. \u201cIs Epicurean Friendship Altruistic?\u201d _Apeiron: A Journal for Ancient Philosophy and Science_ 34 (4): 269\u2013306. http://www.degruyter.com/dg/viewarticle.fullcontentlink:pdfeventlink/$002fj$002fapeiron.2001.34.4$002fapeiron.2001.34.4.269$002fapeiron.2001.34.4.269.xml?t:ac=j$002fapeiron.2001.34.4$002fapeiron.2001.34.4.269$002fapeiron.2001.34.4.269.xml."

EXPECTED_RTF_COLL = '\xabclass RTF \xbb:\xabdata RTF 7B5C727466315C616E73695C616E7369637067313235325C636F636F61727466313236355C636F636F617375627274663231300A7B5C666F6E7474626C5C66305C66726F6D616E5C6663686172736574302054696D65732D526F6D616E3B7D0A7B5C636F6C6F7274626C3B5C7265643235355C677265656E3235355C626C75653235353B7D0A5C6465667461623732300A5C706172645C7061726465667461623732300A0A5C66305C66733234205C6366302043696365726F2C204D61726375732054756C6C6975732E20323030312E200A5C692043696365726F3A204F6E204D6F72616C20456E64730A5C6930202E20456469746564206279204A756C696120416E6E61732E205472616E736C61746564206279205261706861656C20576F6F6C662E2043616D62726964676520556E69766572736974792050726573732E5C0A4465204C6163792C205068696C6C69702E20313935372E205C27393350726F6365737320616E642056616C75653A20416E2045706963757265616E2044696C656D6D612E5C27393420496E200A5C69205472616E73616374696F6E7320616E642050726F63656564696E6773206F662074686520416D65726963616E205068696C6F6C6F676963616C204173736F63696174696F6E0A5C6930202C2038383A3131345C27393632362E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F31302E323330372F3238333839372E5C0A4465204C6163792C205068696C6C697020486F776172642E20313934382E205C2739334C756372657469757320616E642074686520486973746F7279206F662045706963757265616E69736D2E5C27393420496E200A5C69205472616E73616374696F6E7320616E642050726F63656564696E6773206F662074686520416D65726963616E205068696C6F6C6F676963616C204173736F63696174696F6E0A5C6930202C2031325C27393632332E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F31302E323330372F3238333335302E5C0A416E6E61732C204A756C69612E20313939352E200A5C6920546865204D6F72616C697479206F662048617070696E6573730A5C6930202E204F78666F726420556E69766572736974792050726573732C205553412E20687474703A2F2F626F6F6B732E676F6F676C652E636F6D2F626F6F6B733F686C3D656E266C723D2669643D4B526677536A6B3366426343266F693D666E642670673D5041332664713D416E6E61732C2B5468652B4D6F72616C6974792B2B6F662B48617070696E6573266F74733D4D57666F62776B6D4737267369673D794432676C3953496E592D5373713278616F7333473267365855732E5C0A436F6F7065722C204A6F686E204D2E20313939352E205C27393345756461696D6F6E69736D20616E64207468652041707065616C20746F204E617475726520696E20746865204D6F72616C697479206F662048617070696E6573733A20436F6D6D656E7473206F6E204A756C696120416E6E61732C20546865204D6F72616C697479206F662048617070696E6573732E5C273934200A5C69205068696C6F736F70687920616E64205068656E6F6D656E6F6C6F676963616C2052657365617263680A5C693020203535202833293A203538375C27393639382E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F31302E323330372F323130383434302E5C0A416E6E61732C204A756C69612E20323031312E205C27393345706963757265616E20456D6F74696F6E732E5C273934200A5C6920477265656B2C20526F6D616E2C20616E642042797A616E74696E6520537475646965730A5C693020203330202832293A203134355C27393636342E20687474703A2F2F677262732E6C6962726172792E64756B652E6564752F61727469636C652F766965772F343236312F302E5C0A4469656C732C204865726D616E6E2E20313931372E205C2739335068696C6F64656D6F73205C2764636265722044696520475C276636747465723A204472697474657320427563682028636F6D6D656E74617279292E5C273934200A5C6920416268616E646C756E67656E20446572204B6F6E69676C6963682050726575737369736368656E20416B6164656D6965204465722057697373656E736368616674656E0A5C69302020362E5C0A4469656C732C204865726D616E6E2E20313931372E205C2739335068696C6F64656D6F73205C2764636265722044696520475C276636747465723A20447269747465732042756368202874657874292E5C273934200A5C6920416268616E646C756E67656E20446572204B6F6E69676C6963682050726575737369736368656E20416B6164656D6965204465722057697373656E736368616674656E0A5C69302020342E5C0A417272696768657474692C204772617A69616E6F2E20313936312E205C27393346696C6F64656D6F2C20446520646973204949492C20636F6C2E20584949202D20584949492C32302E5C273934200A5C6920537475646920636C6173736963692065206F7269656E74616C690A5C6930202031303A203131325C27393632312E5C0A417272696768657474692C204772617A69616E6F2E20313935382E205C27393346696C6F64656D6F2C20446520646973204949492C20636F6C2E2058202D2058492E5C273934200A5C6920537475646920636C6173736963692065206F7269656E74616C690A5C69302020373A2038335C27393639392E5C0A436C61792C204469736B696E2E20313939382E205C273933496E646976696475616C20616E6420436F6D6D756E69747920696E207468652046697273742047656E65726174696F6E206F66207468652045706963757265616E205363686F6F6C2E5C27393420496E200A5C692050617261646F736973202620537572766976616C3A20546872656520436861707465727320696E2074686520486973746F7279206F662045706963757265616E205068696C6F736F7068790A5C6930202C2035355C27393637342E20416E6E3A20556E6976657273697479206F66204D6963686967616E2050726573732E5C0A436C61792C204469736B696E2E20313939382E200A5C692050617261646F736973202620537572766976616C3A20546872656520436861707465727320696E2074686520486973746F7279206F662045706963757265616E205068696C6F736F7068790A5C6930202E20556E6976657273697479206F66204D6963686967616E2050726573732E20687474703A2F2F7777772E676F6F676C652E636F6D2F626F6F6B733F686C3D656E266C723D2669643D7158526F4439625965393043266F693D666E642670673D505231372664713D50617261646F7369732B616E642B537572766976616C266F74733D4C4F7534444A626F4B62267369673D6E59634A67355474614F6D305F53574F70314970427443786E49302E5C0A41726D7374726F6E672C2044617669642E20323031312E205C27393345706963757265616E20566972747565732C2045706963757265616E20467269656E64736869703A2043696365726F207673207468652048657263756C616E65756D205061707972692E5C27393420496E200A5C6920457069637572757320616E64207468652045706963757265616E20547261646974696F6E0A5C6930202C20656469746564206279204A656666726579204669736820616E64204B69726B20522E2053616E646572732C203130355C27393632382E2043616D6272696467653A2043616D62726964676520556E69766572736974792050726573732E5C0A466973682C204A6566667265792C20616E64204B69726B20522E2053616E646572732C206564732E20323031312E200A5C6920457069637572757320616E64207468652045706963757265616E20547261646974696F6E0A5C6930202E2043616D62726964676520556E69766572736974792050726573732E5C0A4576616E732C204D6174746865772E20323030342E205C27393343616E2045706963757265616E7320426520467269656E64733F5C273934200A5C6920416E6369656E74205068696C6F736F7068790A5C693020203234202832293A203430375C27393632342E20687474703A2F2F7777772E7068696C6F736F706869652E756E692D6D75656E6368656E2E64652F6C65687265696E68656974656E2F7068696C6F736F706869655F332F706572736F6E656E2F6861737065722F766572675F73656D2F6C765F736F73655F323031312F667265756E647363686166742F6576616E735F6570696375725F667265756E642E7064662E5C0A537465726E2D47696C6C65742C2053757A616E6E652E20313938392E205C273933457069637572757320616E6420467269656E64736869702E5C273934200A5C69204469616C6F6775653A2043616E616469616E205068696C6F736F70686963616C205265766965772F52657675652043616E616469656E6E65206465205068696C6F736F706869650A5C69302020323820283032293A203237355C27393638382E20646F693A31302E313031372F53303031323231373330303031353737382E5C0A576865656C65722C204D2E20522E20323030332E205C2739334570696375727573206F6E20467269656E64736869703A2054686520456D657267656E6365206F6620426C65737365646E6573732E5C27393420496E200A5C692045706963757275733A2048697320436F6E74696E75696E6720496E666C75656E636520616E6420436F6E74656D706F726172792052656C6576616E63650A5C6930202C206564697465642062792044616E6520522E20476F72646F6E20616E6420446176696420422E2053756974732C203138335C27393639342E205249542043617279204772617068696320417274732050726573732E5C0A476F72646F6E2C2044616E6520522E2C20616E6420446176696420422E2053756974732C206564732E20323030332E200A5C692045706963757275733A2048697320436F6E74696E75696E6720496E666C75656E636520616E6420436F6E74656D706F726172792052656C6576616E63650A5C6930202E205249542043617279204772617068696320417274732050726573732E5C0A4D69747369732C205068696C6C69702E20313938392E200A5C6920457069637572757327204574686963616C205468656F72793A2054686520506C65617375726573206F6620496E76756C6E65726162696C6974790A5C6930202E20436F726E656C6C20556E69766572736974792050726573732E20687474703A2F2F7777772E616D617A6F6E2E63612F657865632F6F6269646F732F72656469726563743F7461673D63697465756C696B6530392D323026706174683D4153494E2F303830313432313837582E5C0A4769616E6E616E746F6E692C204761627269656C652C204D617263656C6C6F20476967616E74652C20616E64204672616E636573636120416C657373652E20313939362E200A5C69204570696375726569736D6F20477265636F204520526F6D616E6F3A20417474692044656C20436F6E67726573736F20496E7465726E617A696F6E616C653A204E61706F6C692C2031392D32365C2761304D616767696F2031393933202F20612043757261204469204761627269656C65204769616E6E616E746F6E692045204D617263656C6C6F20476967616E74650A5C6930202E204E61706F6C693A204269626C696F706F6C69732E5C0A4B6F6E7374616E2C2044617669642E20313939362E205C273933467269656E64736869702066726F6D20457069637572757320746F205068696C6F64656D75732E5C27393420496E200A5C69204570696375726569736D6F20477265636F204520526F6D616E6F0A5C6930202E204269626C696F706F6C69732E5C0A546869626F646561752C205068696C69702E20323030332E205C27393343616E2056657267696C204372793F2045706963757265616E69736D20696E20486F72616365204F64657320312E32342E5C273934200A5C692054686520436C6173736963616C204A6F75726E616C0A5C693020203938202833293A203234335C2739363235362E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F333239383034372E5C0A536E796465722C204A616E65204D63496E746F73682E20313937332E205C27393354686520506F65747279206F66205068696C6F64656D7573207468652045706963757265616E2E5C273934200A5C692054686520436C6173736963616C204A6F75726E616C0A5C693020203638202834293A203334365C2739363335332E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F333239353935382E5C0A4465576974742C204E6F726D616E20572E20313933372E205C2739335468652045706963757265616E20446F637472696E65206F66204772617469747564652E5C273934200A5C692054686520416D65726963616E204A6F75726E616C206F66205068696C6F6C6F67790A5C693020203538202833293A203332305C2739363332382E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F3239303333302E5C0A4465576974742C204E6F726D616E20572E20313933362E205C27393345706963757265616E20436F6E74756265726E69756D2E5C273934200A5C69205472616E73616374696F6E7320616E642050726F63656564696E6773206F662074686520416D65726963616E205068696C6F6C6F676963616C204173736F63696174696F6E0A5C6930202036373A2035355C27393636332E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F3238333232372E5C0A41726D7374726F6E672C204A6F686E204D2E20313939372E205C27393345706963757265616E204A7573746963652E5C273934200A5C69205068726F6E657369730A5C693020203432202833293A203332345C2739363333342E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F343138323536372E5C0A4B656974682C20417274687572204C2E20313932392E205C27393343696365726F27732049646561206F6620467269656E64736869702E5C273934200A5C692054686520536577616E6565205265766965770A5C693020203337202831293A2035315C27393635382E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F32373533343335352E5C0A46617272696E67746F6E2C20422E20313935342E205C2739334C756372657469757320616E64204D616E696C697573206F6E20467269656E64736869702E5C273934200A5C69204865726D617468656E610A5C6930202C206E6F2E2038333A2031305C27393631362E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F32333033393331352E5C0A42726F776E2C20457269632E20323030322E205C2739334570696375727573206F6E207468652056616C7565206F6620467269656E647368697020285C27393153656E74656E746961205661746963616E6127203233292E5C273934200A5C6920436C6173736963616C205068696C6F6C6F67790A5C693020203937202831293A2036385C27393638302E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F313231353534372E5C0A526973742C204A6F686E204D2E20313938302E205C2739334570696375727573206F6E20467269656E64736869702E5C273934200A5C6920436C6173736963616C205068696C6F6C6F67790A5C693020203735202832293A203132315C2739363132392E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F3236383931392E5C0A416C6C656E2C2057616C7465722C204A722E20313933382E205C2739334F6E2074686520467269656E6473686970206F66204C75637265746975732077697468204D656D6D6975732E5C273934200A5C6920436C6173736963616C205068696C6F6C6F67790A5C693020203333202832293A203136375C2739363138312E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F3236333937362E5C0A48616C6C2C20436C6179746F6E204D2E20313933352E205C273933536F6D652045706963757265616E7320617420526F6D652E5C273934200A5C692054686520436C6173736963616C205765656B6C790A5C69302020323820283135293A203131335C2739363131352E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F343333393530312E5C0A506F727465722C204A616D657320492E20323030332E205C27393345706963757265616E204174746163686D656E74733A204C6966652C20506C6561737572652C204265617574792C20467269656E64736869702C20616E642050696574792E5C273934200A5C692043726F6E61636865204572636F6C616E6573690A5C693020203230303320283333293A203230355C27393632332E5C0A4F27436F6E6E6F722C204461766964204B2E20323031312E205C27393354686520496E76756C6E657261626C6520506C65617375726573206F662045706963757265616E20467269656E64736869702E5C273934200A5C6920477265656B2C20526F6D616E2C20616E642042797A616E74696E6520537475646965730A5C693020203330202832293A203136355C27393638362E2068747470733A2F2F6F70656E7075626C697368696E672E6C6962726172792E64756B652E6564752F696E6465782E7068702F677262732F61727469636C652F7669657741727469636C652F343237312E5C0A5475726E65722C204A2E2048696C746F6E2E20313934372E205C273933457069637572757320616E6420467269656E64736869702E5C273934200A5C692054686520436C6173736963616C204A6F75726E616C0A5C693020203432202836293A203335315C27393635362E20687474703A2F2F7777772E6A73746F722E6F72672F737461626C652F31302E323330372F333239313634362E5C0A4F274B656566652C2054696D2E20323030312E205C27393349732045706963757265616E20467269656E647368697020416C74727569737469633F5C273934200A5C692041706569726F6E3A2041204A6F75726E616C20666F7220416E6369656E74205068696C6F736F70687920616E6420536369656E63650A5C693020203334202834293A203236395C2739363330362E20687474703A2F2F7777772E6465677275797465722E636F6D2F64672F7669657761727469636C652E66756C6C636F6E74656E746C696E6B3A7064666576656E746C696E6B2F24303032666A243030326661706569726F6E2E323030312E33342E34243030326661706569726F6E2E323030312E33342E342E323639243030326661706569726F6E2E323030312E33342E342E3236392E786D6C3F743A61633D6A243030326661706569726F6E2E323030312E33342E34243030326661706569726F6E2E323030312E33342E342E323639243030326661706569726F6E2E323030312E33342E342E3236392E786D6C2E5C0A7D\xbb'
## -----------------------------------------------------------------------------

EXPECTED_MD_TAG = 'Falconer, Kenneth. 2004. _Fractal Geometry: Mathematical Foundations and Applications_. John Wiley & Sons.'

EXPECTED_RTF_TAG = '\xabclass RTF \xbb:\xabdata RTF 7B5C727466315C616E73695C616E7369637067313235325C636F636F61727466313236355C636F636F617375627274663231300A7B5C666F6E7474626C5C66305C66726F6D616E5C6663686172736574302054696D65732D526F6D616E3B7D0A7B5C636F6C6F7274626C3B5C7265643235355C677265656E3235355C626C75653235353B7D0A5C6465667461623732300A5C706172645C7061726465667461623732300A0A5C66305C66733234205C6366302046616C636F6E65722C204B656E6E6574682E20323030342E200A5C69204672616374616C2047656F6D657472793A204D617468656D61746963616C20466F756E646174696F6E7320616E64204170706C69636174696F6E730A5C6930202E204A6F686E2057696C6579202620536F6E732E5C0A7D\xbb'


ZQ = '/Users/smargheim/Documents/DEVELOPMENT/GitHub/ZotQuery/testing_env/workflow_dir/zotquery.py'

def setUp():
    pass

def tearDown():
    pass


def capture_output(zot_filter):
    """Capture `sys` output in var"""
    res_dict = xmltodict.parse(zot_filter)
    if res_dict['items'] == None:
        uids = []
    elif isinstance(res_dict['items']['item'], list):
        uids = [x['arg'] for x in res_dict['items']['item']]
    elif isinstance(res_dict['items']['item'], OrderedDict):
        uids = [res_dict['items']['item']['arg']]
    return uids

class FilterTests(unittest.TestCase):
    """Test the Filters"""

    ####################################################################
    # Filter Tests
    ####################################################################

    # General Scope ----------------------------------------------
    def test_filter_general(self):
        """Test `general` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'general', 'margheim'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_3KFT2HQ9', '0_C3KEUQJW'])
    
    # Creators Scope ----------------------------------------------
    def test_filter_creators(self):
        """Test `creators` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'creators', 'rosen'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_7VPPEPGQ', '0_MK8GBNFH', '0_3G9MDISQ'])

    # Titles Scope ----------------------------------------------
    def test_filter_titles(self):
        """Test `titles` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'titles', 'fractal math'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_I6GVRQN7'])

    # Notes Scope ----------------------------------------------
    def test_filter_notes(self):
        """Test `notes` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'notes', 'heraclitus'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_R2CXZ4JM'])

    # Collections Scope ----------------------------------------------
    def test_filter_collections_len(self):
        """Test `collections` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'collections', 'epi'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['c_GXWGBRJD', 'c_K4Q262P7', 'c_5JBVB4Q4'])

    # Tags Scope ----------------------------------------------
    def test_filter_tags(self):
        """Test `tags` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'tags', 'math'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['t_5NVC3T2F', 't_P89IJCMX'])

    # In-Collection Scope ----------------------------------------------
    def test_filter_incollection(self):
        """Test `in-collection` scope"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                'store', 'collection', 'c_GXWGBRJD'])
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'in-collection', 'cicero'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_UD7N4Z35', '0_GKXR98CF', '0_AGX7WZDQ'])

    # In-Tag Scope ----------------------------------------------
    def test_filter_intag(self):
        """Test `in-tag` scope"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                'store', 'tag', 't_P89IJCMX'])
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'in-tag', 'geometr'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_I6GVRQN7'])

    # Attachments Scope ----------------------------------------------
    def test_filter_attachment(self):
        """Test `attachments` scope"""
        zot_filter = subprocess.check_output(['/usr/bin/python', ZQ,
                                'search', 'attachments', 'reguero'])
        uids = capture_output(zot_filter)
        self.assertEqual(uids,
                         ['0_MBXHR545'])



class MDActionTests(unittest.TestCase):

    def setUp(self):
        prefs = {"fmt": "Markdown",
                 "csl": "chicago-author-date",
                 "app": "Standalone"}
        utils.json_write(prefs, '/Users/smargheim/Documents/DEVELOPMENT/GitHub/ZotQuery/testing_env/storage_dir/output_settings.json')


    ####################################################################
    # Action Tests
    ####################################################################

    def test_action_export_citation(self):
        """Test full citation action"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                 'export', 'bib', '0_MBXHR545'])
        self.assertEqual(utils.get_clipboard(),
            'Reguero, M. Carmen Encinas. 2009. \u201cLa Evoluci\xf3n de Algunos Conceptos Ret\xf3ricos. Semeion Y Tekmerion Del S. V Al IV a.C.\u201d *Rhetorica* 27 (4): 373\u2013403. doi:10.1525/RH.2009.27.4.373.')

    def test_action_export_ref(self):
        """Test full citation action"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                 'export', 'citation', '0_5SFSEF7M'])
        self.assertEqual(utils.get_clipboard(),
            '(Bodn\xe1r and Fortenbaugh 2002)')

    def test_action_export_collection(self):
        """Test full citation action"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                 'export', 'group', 'c_GXWGBRJD'])
        self.assertEqual(utils.get_clipboard(),
            EXPECTED_MD_COLL)

    def test_action_export_tag(self):
        """Test full citation action"""
        subprocess.check_output(['/usr/bin/python', ZQ,
                                 'export', 'group', 't_P89IJCMX'])
        self.assertEqual(utils.get_clipboard(),
            EXPECTED_MD_TAG)




if __name__ == '__main__':
    unittest.main()