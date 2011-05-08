# -*- coding: utf-8 -*-
import collective.setuphandlertools as sht
import logging
from Products.ATContentTypes.lib import constraintypes
logger = logging.getLogger("thet.helsinki.base")

def setup_content(context):
    if sht.isNotThisProfile(context, 'thet.helsinki.base-setup_content.txt'):
        return

    site = context.getSite()

    sht.delete_items(site, ('front-page', 'news', 'events'), logger)
    sht.hide_and_retract(site['Members'], hide=False, logger=logger)

    sht.add_group(site, 'vorstand', roles=['Member'], logger=logger)
    sht.add_group(site, 'office', roles=['Member'], logger=logger)
    sht.add_group(site, 'programmrat', roles=['Member'], logger=logger)
    sht.add_group(site, 'technik', roles=['Member'], logger=logger)
    sht.add_user(site, 'thet', 'thet',
                 email='johannes@raggam.co.at', fullname="Johannes Raggam",
                 groups=['vorstand'], logger=logger)

    content_structure = [
        {'type': 'Topic', 'title':u'News',
         'opts': {'setLayout': 'folder_summary_view',
                  'setDefault': True,}
        },
        {'type': 'Folderish Document', 'title':u'Livestream',
         'data':{'description':LIVESTREAM_DESC, 'text':LIVESTREAM_TEXT}},
        {'type': 'Folder', 'title': u'Programm',
         'opts': {'setLayout': 'traverse_view',},
         'childs': [
             {'type': 'Folder', 'id':u'today', 'title':u'Tagesansicht'},
             {'type': 'Folder', 'id':u'week', 'title':u'Wochenansicht'},
             {'type': 'Folder', 'id':u'shows', 'title':u'Sendungen'},
             {'type': 'Folder', 'id':u'hosts', 'title':u'SendungsmacherInnen'},
             {'type': 'Folder', 'id':u'tips', 'title':u'Tipps'},
             {'type': 'Folderish Document', 'title':u'Programmflyer'},
             {'type': 'Link', 'title':u'Programmverwaltung',
              'data':{'remoteUrl':u'https://pv.helsinki.at/admin/'},
              'opts': {'workflow': None,}}, # leave private
        ]},
        {'type': 'Folder', 'title': u'Info', 'childs': [
            {'type': 'Folderish Document', 'title':u'Kontakt',
             'data':{'text':KONTAKT_TEXT}},
            {'type': 'Folderish Document', 'title':u'Über uns', 'childs':[
                {'type': 'Folderish Document', 'title':u'Charta der freien Radios',
                 'data':{'text':CHARTA_TEXT}},
                {'type': 'Folderish Document', 'title':u'Geschichte'},
                {'type': 'Folderish Document', 'title':u'Gremien'},
                {'type': 'Folder', 'title':u'Bildergalerien'},
            ]},
            {'type': 'Folderish Document', 'title':u'Mitmachen'},
            {'type': 'Folderish Document', 'title':u'Unterstützen'},
            {'type': 'Link', 'title':u'Wiki',
                'data':{'remoteUrl':u'https://intranet.helsinki.at/wiki/'}
            },
            {'type': 'Folderish Document', 'title':u'Logo'},
            {'type': 'Folderish Document', 'title':u'Impressum'},
        ]},
        {'type': 'Folder', 'title': u'Projekte',
         'opts': {'setLayout': 'traverse_view',
                  'setLocallyAllowedTypes': ['Project'],
                  'setImmediatelyAddableTypes': ['Project']},
         'childs':[
             {'type': 'Topic', 'title':u'Aktuelles',
              'opts': {'setLayout': 'folder_summary_view',}},
             {'type': 'Topic', 'title':u'Kommendes',
              'opts': {'setLayout': 'folder_summary_view',}},
             {'type': 'Topic', 'title':u'Vergangenes',
              'opts': {'setLayout': 'folder_summary_view',}},
        ]},
    ]
    sht.create_item_runner(site, content_structure, lang='de', logger=logger)


    #site.setConstrainTypesMode(constraintypes.ENABLED)
    #site.setLocallyAllowedTypes(item['opts']['setLocallyAllowedTypes'])
    #site.setImmediatelyAddableTypes(['Teaser', 'Folderish News Item',])
    import pdb;pdb.set_trace()
    try:
        topic = site['news']
        topic.limitNumber = True
        topic.itemCount = 10
        type_crit = topic.addCriterion('Type','ATPortalTypeCriterion')
        type_crit.setValue(['News Item with Folder', 'News Item'])
        topic.reindexObject()
        logger.info('configured topic %s' % topic.id)
    except:
        pass

    try:
        topic = site['projekte']['aktuelles']
        topic.limitNumber = True
        topic.itemCount = 10
        type_crit = topic.addCriterion('Type','ATPortalTypeCriterion')
        type_crit.setValue(['Project'])
        sort_crit = topic.addCriterion('start','ATSortCriterion')
        start_crit = topic.addCriterion('start', 'ATFriendlyDateCriteria')
        start_crit.setValue(0)
        start_crit.setDateRange('-')
        start_crit.setOperation('less')
        end_crit = topic.addCriterion('end', 'ATFriendlyDateCriteria')
        end_crit.setValue(0)
        end_crit.setDateRange('+')
        end_crit.setOperation('more')
        topic.reindexObject()
        logger.info('configured topic %s' % topic.id)
    except:
        pass

    try:
        topic = site['projekte']['kommendes']
        topic.limitNumber = True
        topic.itemCount = 10
        type_crit = topic.addCriterion('Type','ATPortalTypeCriterion')
        type_crit.setValue(['Project'])
        sort_crit = topic.addCriterion('start','ATSortCriterion')
        date_crit = topic.addCriterion('start', 'ATFriendlyDateCriteria')
        date_crit.setValue(0)
        date_crit.setDateRange('+')
        date_crit.setOperation('more')
        topic.reindexObject()
        logger.info('configured topic %s' % topic.id)
    except:
        pass

    try:
        topic = site['projekte']['vergangenes']
        topic.limitNumber = True
        topic.itemCount = 10
        type_crit = topic.addCriterion('Type','ATPortalTypeCriterion')
        type_crit.setValue(['Project'])
        sort_crit = topic.addCriterion('start','ATSortCriterion')
        sort_crit.setReversed(True)
        date_crit = topic.addCriterion('end', 'ATFriendlyDateCriteria')
        date_crit.setValue(0)
        date_crit.setDateRange('-')
        date_crit.setOperation('less')
        topic.reindexObject()
        logger.info('configured topic %s' % topic.id)
    except:
        pass


# setup testdata
def setup_testdata(context):
    """Setup Test Content for Website
    """
    if sht.isNotThisProfile(context, 'thet.helsinki.base-setup_testdata.txt'): return
    site = context.getSite()

    # news
    ctx = site
    content_structure = [
        {'type': 'Folderish News Item', 'title': u'Gegen ein Bettelverbot in der Steiermark',
         'data':{
             'description':u"""Die Plattform gegen ein Bettelverbot in der Steiermark hat zum PROTEST aufgerufen.""",
             'image':sht.load_file(globals(), 'data/bettelverbot/181571_1697638692197_1574763386_1607041_6303679_n.jpg'),
             'imageCaption':u'Wir setzen uns nieder!',
             'text':u"""
<p><b>"Wir setzen uns nieder!"</b> war das Motto, unter dem sich am  Samstag, 12. Februar 2011 ab 11 Uhr mehrere hundert Menschen in der  Grazer Herrengasse vor dem Landhaus zum Protest trafen. <br /><br /> Die Plattform ist ein überparteilicher Zusammenschluss von Initiativen  gegen die Verschärfung des Landessicherheitsgesetzes und die Einführung  eines Bettelverbotes in der Steiermark. Am Dienstag, den 15. Februar,  wurde ein generelles Bettelverbot im steirischen Landtag beschlossen.  <br /><br /> Das können wir nicht hinnehmen. Dagegen stehen wir auf. Dagegen setzen wir uns nieder!  <br /><br /> * Die Straße gehört uns allen!<br /> * Betteln ist ein Menschenrecht für Menschen in Not<br /> * Gegen die Vertreibung der Roma! <br /><br /> Die Besetzung der Herrengasse am 12.2. war ein mächtiges Zeichen der Zivilgesellschaft in dieser Stadt. <br /><br /> Die Plattform wird getragen von (Stand 10.2.2011): <br /> Akademie Graz<br /> Dachverband der offenen Jugendarbeit<br /> DIDF - Föderation der Demokratischen Arbeitervereine<br /> dramagraz<br /> Elevate<br /> ETC Europäisches Trainings- und Forschungszentrum<br /> Forschungsteam „Shifting romipen” (Uni Graz)<br /> Forum Stadtpark<br /> Freigangproduktionen<br /> Die Grünen (Graz u. Steiermark)<br /> Grazer Initiative<br /> IG Kultur Steiermark<br /> Innovative Sozialprojekte – ISOP<br /> Jugendkulturzentrum Explosiv<br /> KPÖ Steiermark<br /> Lendwirbel<br /> Megaphon<br /> Grazer Menschenrechtsbeirat<br /> ÖH der Karl-Franzens Universität Graz<br /> Pfarre St. Andrä<br /> Radio Helsinki<br /> &lt; rotor &gt; Verein für zeitgenössische Kunst<br /> Spektral<br /> [spi:k] - Verein zur Dokumentation der Sprache und Kultur regionaler Minderheiten<br /> steirischer herbst<br /> the smallest gallery – collaboration space<br /> Theater am Ortweinplatz<br /> Theater im Bahnhof<br /> Vinzenzgemeinschaft Eggenberg<br /> Welthaus Diözese Graz-Seckau<br /> Xenos - Verein zur Förderung der Soziokulturellen Vielfalt<br /> … <br /><br /> Und DIR! <br /><br /> Plattform gegen ein Bettelverbot in der Steiermark<br /> Kontakt: gegenbettelverbot@gmail.com <br /> Facebook-Gruppe: <a href="http://www.facebook.com/group.php?gid=121805051185095">Gegen ein Bettelverbot in Graz</a></p>
             """},
             'childs': [
                 {'type': 'Folder', 'title': u'Bildergalerie',
                  'opts': {'setLayout': u'gallery.html'},
                  'childs': [
{'type': 'Image', 'title': u'bild1', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/168351_1697643132308_1574763386_1607057_8004618_n.jpg')}},
{'type': 'Image',  'title': u'bild2', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/168387_1697641732273_1574763386_1607052_5112999_n.jpg')}},
{'type': 'Image',  'title': u'bild3', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/168915_1697641852276_1574763386_1607053_121061_n.jpg')}},
{'type': 'Image',  'title': u'bild4', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/168967_1697642892302_1574763386_1607056_521602_n.jpg')}},
{'type': 'Image',  'title': u'bild5', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/179811_1697641572269_1574763386_1607051_3501510_n.jpg')}},
{'type': 'Image',  'title': u'bild6', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/179827_1697637852176_1574763386_1607035_7117248_n.jpg')}},
{'type': 'Image',  'title': u'bild7', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180023_1697640172234_1574763386_1607046_4574419_n.jpg')}},
{'type': 'Image',  'title': u'bild8', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180043_1697642292287_1574763386_1607054_5640632_n.jpg')}},
{'type': 'Image',  'title': u'bild9', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180067_191519290866152_100000242460345_616154_2974335_n.jpg')}},
{'type': 'Image',  'title': u'bild10', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180115_1697635772124_1574763386_1607021_8195464_n.jpg')}},
{'type': 'Image',  'title': u'bild11', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180347_1697639852226_1574763386_1607045_2264331_n.jpg')}},
{'type': 'Image',  'title': u'bild12', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180351_1697640812250_1574763386_1607048_6149618_n.jpg')}},
{'type': 'Image',  'title': u'bild13', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180375_1697641172259_1574763386_1607049_895722_n.jpg')}},
{'type': 'Image',  'title': u'bild14', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180571_1697638292187_1574763386_1607039_1981472_n.jpg')}},
{'type': 'Image',  'title': u'bild15', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180751_1697643492317_1574763386_1607059_553489_n.jpg')}},
{'type': 'Image',  'title': u'bild16', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180811_1697639292212_1574763386_1607044_7345632_n.jpg')}},
{'type': 'Image',  'title': u'bild17', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180839_194623570565826_100000545529524_640338_4974991_n.jpg')}},
{'type': 'Image',  'title': u'bild18', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/180863_1697643332313_1574763386_1607058_1679619_n.jpg')}},
{'type': 'Image',  'title': u'bild19', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/181571_1697638692197_1574763386_1607041_6303679_n.jpg')}},
{'type': 'Image',  'title': u'bild20', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182399_1697636332138_1574763386_1607025_2307995_n.jpg')}},
{'type': 'Image',  'title': u'bild21', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182431_1697638892202_1574763386_1607042_6760018_n.jpg')}},
{'type': 'Image',  'title': u'bild22', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182431_1697642692297_1574763386_1607055_1838171_n.jpg')}},
{'type': 'Image',  'title': u'bild23', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182466_1854570602312_1182212188_32287621_7037162_n.jpg')}},
{'type': 'Image',  'title': u'bild24', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182827_1697636772149_1574763386_1607029_7992200_n.jpg')}},
{'type': 'Image',  'title': u'bild25', 'data':{'image':sht.load_file(globals(), 'data/bettelverbot/182875_1697637132158_1574763386_1607032_4319304_n.jpg')}},

              ]}]},

              {'type': 'Folderish News Item', 'title': u'Sendungen on demand"',
               'data':{
               'description':u"""
Sendung verpasst? Lust auf nochmal Hören? Das geht (immer öfter). Viele
Sendungen von Radio Helsinki sind online verfügbar. Eine Auswahl...
               """,
               'image':sht.load_file(globals(), 'data/EUVE_satellite.gif'),
               'text':u"""
<p>Abunda Lingva <a href="http://cba.fro.at/series/978" target="_blank">http://cba.fro.at/</a> <br /> A_partment politi_X <a href="http://www.freie-radios.net/portal/suche.php?such=true&amp;query=&amp;redaktion=0&amp;art=0&amp;serie=129&amp;sprache=0&amp;radio=0&amp;autor=&amp;beg_monat=01&amp;beg_jahr=1970&amp;end_monat=12&amp;end_jahr=2011&amp;Submit=Suche+starten" target="_blank">http://www.freie-radios.net/</a> <br /> bitte8bit <a href="http://cba.fro.at/series/607" target="_blank">http://cba.fro.at/</a> <br /> clash connect <a href="http://cba.fro.at/series/884" target="_blank">http://cba.fro.at/</a> <br /> COCOYOC  <a href="http://cba.fro.at/series/877" target="_blank">http://cba.fro.at/</a> <br /> CROPfm <a href="http://cropfm.at/past_shows.htm" target="_blank">http://cropfm.at/</a> <br /> gender frequenz <a href="http://cba.fro.at/series/966" target="_blank">http://cba.fro.at/</a> <br /> Hörbar Abstrakt <a href="http://www.kim-pop.org/index.cfm?contentURL=http%3A//www.kim-pop.org/index.cfm%3Ffuseaction%3Dintro" target="_blank">http://www.kim-pop.org/</a> <br /> Hör-Saal <a href="http://cba.fro.at/series/1045" target="_blank">http://cba.fro.at/</a> <br /> In Graz verstrickt <a href="http://cba.fro.at/series/948" target="_blank">http://cba.fro.at/</a> <br /> Klimanews <a href="http://cba.fro.at/series/685" target="_blank">http://cba.fro.at/</a> <br /> Put a bullet thru the jukebox <a href="http://cba.fro.at/series/571" target="_blank">http://cba.fro.at/</a> <br /> Radio Auslandsdienst <a href="http://radio.auslandsdienst.at/sendungen/" target="_blank">http://radio.auslandsdienst.at/</a> <br /> Stimmen aus dem Annenviertel <a href="http://cba.fro.at/series/774" target="_blank">http://cba.fro.at/</a> <br /> Tonspur <a href="http://sendungtonspur.wordpress.com/" target="_blank">http://tonspur.mur.at/</a> <br /> Wissen <a href="http://www-gewi.uni-graz.at/cocoon/pug/gsearch?query=Helsinki&amp;query_encoded=Helsinki&amp;hitPageStart=1&amp;hitPageSize=10" target="_blank">Podcast-Portal Uni Graz</a></p>
               """}},
    ]
    sht.create_item_runner(ctx, content_structure, lang='de', logger=logger)

    # galleries
    ctx = site['info']['uber-uns']['bildergalerien']
    content_structure = [
        {'type': 'Folder', 'title': u'Das Radio',
         'opts': {'setLayout': u'gallery.html'},
         'data':{'description':u"""Bilder vom Studio in der Griesgasse."""},
         'childs':[
{'type': 'Image',  'title': u'bild1', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_aus_dem_Studio.jpg')}},
{'type': 'Image',  'title': u'bild2', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_Buero.jpg')}},
{'type': 'Image',  'title': u'bild3', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_Eingang_mit_Menschen.jpg')}},
{'type': 'Image',  'title': u'bild4', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_foyer.jpg')}},
{'type': 'Image',  'title': u'bild5', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_im_Studio.jpg')}},
{'type': 'Image',  'title': u'bild6', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_Kinder_machen_Radio.jpg')}},
{'type': 'Image',  'title': u'bild7', 'data':{'image':sht.load_file(globals(), 'data/radio/RadioHelsinki_Redaktionsraum.jpg')}},
        ]},

        {'type': 'Folder', 'title': u'Das alte Radio',
         'opts': {'setLayout': u'gallery.html'},
         'data':{'description':u"""Bilder vom alten Studio in der Schörgelgasse."""},
         'childs':[
{'type': 'Image',  'title': u'bild1', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/andrea.jpg')}},
{'type': 'Image',  'title': u'bild2', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/botanik.jpg')}},
{'type': 'Image',  'title': u'bild3', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/eingang.jpg')}},
{'type': 'Image',  'title': u'bild4', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/franz.jpg')}},
{'type': 'Image',  'title': u'bild5', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/sessel.jpg')}},
{'type': 'Image',  'title': u'bild6', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/studio1.jpg')}},
{'type': 'Image',  'title': u'bild7', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/studio2.jpg')}},
{'type': 'Image',  'title': u'bild8', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/studio3.jpg')}},
{'type': 'Image',  'title': u'bild9', 'data':{'image':sht.load_file(globals(), 'data/radio_alt/wuggi-moke.jpg')}},
        ]},

        {'type': 'Folder', 'title': u'Gutshauskranz 2004',
         'opts': {'setLayout': u'gallery.html'},
         'data':{'description':u"""Helsinki Aussenstudio im Rahmen des steirischen herbstes 2004."""},
         'childs':[
{'type': 'Image',  'title': u'bild1', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_EnrLichtweb.jpg')}},
{'type': 'Image',  'title': u'bild2', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Fanfarenweb.jpg')}},
{'type': 'Image',  'title': u'bild3', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Hausterrasse.jpg')}},
{'type': 'Image',  'title': u'bild4', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Hausvonhinten.jpg')}},
{'type': 'Image',  'title': u'bild5', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_MokRobKarKlein.jpg')}},
{'type': 'Image',  'title': u'bild6', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Studiowandweb.jpg')}},
{'type': 'Image',  'title': u'bild7', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Vpweb.jpg')}},
{'type': 'Image',  'title': u'bild8', 'data':{'image':sht.load_file(globals(), 'data/gutshauskranz/RadioHelsinki_Wohnzimmerweb.jpg')}},
         ]},


        {'type': 'Folder', 'title': u'Herbstfest 2006',
         'opts': {'setLayout': u'gallery.html'},
         'data':{'description':u"""Helsinki Herbstfest 2006."""},
         'childs':[
{'type': 'Image',  'title': u'bild1', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Band_Ratlos.jpg')}},
{'type': 'Image',  'title': u'bild2', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Beinand.jpg')}},
{'type': 'Image',  'title': u'bild3', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Buffet.jpg')}},
{'type': 'Image',  'title': u'bild4', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Erwischt_am_Damenklo.jpg')}},
{'type': 'Image',  'title': u'bild5', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Familie_Petz.jpg')}},
{'type': 'Image',  'title': u'bild6', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Gstopft_voll.jpg')}},
{'type': 'Image',  'title': u'bild7', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Hofgewurle.jpg')}},
{'type': 'Image',  'title': u'bild8', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_Maroniman.jpg')}},
{'type': 'Image',  'title': u'bild9', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_MiniSendungsmacher.jpg')}},
{'type': 'Image',  'title': u'bild10', 'data':{'image':sht.load_file(globals(), 'data/herbstfest2006/RadioHelsinki_RoKa.jpg')}},
          ]},
        ]
    sht.create_item_runner(ctx, content_structure, lang='de', logger=logger)



    #projekte
    ctx = site['projekte']
    content_structure = [
        {'type': 'Project', 'title': u'COCOYOC - Entwicklungspolitische Vereine berichten...',
         'data':{
             'start': '2010-01-01 00:00:00 UTC',
             'end': '2011-07-01 00:00:00 UTC',
             'image':sht.load_file(globals(), 'data/cocoyoc/bik.jpg'),
             'text':u"""
<p><a href="http://cba.fro.at/series/877">Download der Sendungen</a><br/>
<a href="http://cba.fro.at/seriesrss/877">RSS Feed der Sendungen</a><br />
<a href="abschlussbericht_eza_stmk_land_web-pdf">Download des Projektberichts 2010</a></p>
<p><b>Entwicklungspolitische Vereine berichten:</b> ...ein  Schulprojekt im Himalaya und im Kongo... Dorfentwicklung und  Solarenergie für Spitäler in Tansania... Wasserkraft für Kuba... ein  Medienprojekt über sexuellen Missbrauch und Stärkung von Frauenrechten  in Nicaragua... ein Brunnenprojekt in Burkina Faso...</p>
<p><b>Freies Radio – Medium der Zivilgesellschaft:</b> Die  Vereine gehören keinen großen (internationalen NGOs, staatlichen oder  kirchlichen) Institutionen an. Die Vereine haben gemeinsam mit Radio  Helsinki Sendungen aus den Projektregionen gestaltet, um alternative und  direkte Informationen (aus der Praxis) zur Entwicklungszusammenarbeit  einer interessierten Öffentlichkeit näher zu bringen.</p>
<p><b>Entwicklungspolitische Praxis</b> findet in pluralen  Räumen statt und hat basale Bedürfnisse zum Inhalt: „Lebensmittel“ sind  Nahrung, Wasser, Medizin, aber auch soziokulturelle oder individuelle  Selbstbestimmung und Bildung. Näher betrachtet, zeigen sich Differenzen,  wie diese Ziele erreicht werden können - sprich: was bedeutet  Entwicklung?</p>
<p><b>COCOYOC - Kontext</b> (Entwicklungspolitische und  Globale Diskurse); Entwicklungspolitische Praxis ist immer unter den jeweils "herrschenden  Verhältnissen" zu verstehen. Auf die historischen, sozialen,  ökonomischen, kulturellen Dimensionen gehen wir in speziellen  Themensendungen ein. Diese Sendungen sind als "Cocoyoc - Kontext"  gekennzeichnet. Zudem treffen sich die Projektvereine, wo wir unsere  Praxis diskutieren und reflektieren.</p>
<p><b>Reichweite der Sendungen:</b> Alle Sendungen sind zum  freien Download (Creative Commons) und für die Verbreitung auf anderen  Freien Radios ins Internet gestellt worden.  Wir danken den Freien  Radios für die Übernahmen von „Cocoyoc Sendungen“:</p>
<p>Campusradio (St. Pölten), <a href="http://www.campusradio.at/">http://www.campusradio.at/</a><br />
Freirad (Innsbruck), <a href="http://www.freirad.at/">http://www.freirad.at/</a><br />
Radiofabrik (Salzburg), <a href="http://www.radiofabrik.at/">http://www.radiofabrik.at/</a><br />
Radio Fro (Linz), <a href="http://www.fro.at/">http://www.fro.at/</a><br />
Proton (Bregenz), <a href="http://www.radioproton.at/">http://www.radioproton.at/</a><br />
Radio Orange (Wien), <a href="http://o94.at/">http://o94.at/</a><br />
coloRadio (Dresden), <a href="http://coloradio.org/">http://coloradio.org/</a><br />
Dreyeckland (Freiburg/Breisgau), <a href="http://www.rdl.de/">http://www.rdl.de/</a><br />
Radio F.R.E.I. (Erfurt), <a href="http://www.radio-frei.de/">http://www.radio-frei.de/</a><br />
Radio Lohro (Rostock), <a href="http://www.lohro.de/">http://www.lohro.de/</a><br />
Radio Lora (Zürich), <a href="http://www.lora.ch/">http://www.lora.ch/</a><br />
</p>

<h2>Die Projektvereine im Überblick</h2>

<h3>Aktion Brücke in den Kongo</h3>
<p><a href="bik-jpg"><img src="bik-jpg/image_mini" style="float: right; " /></a> Aktion Brücke in den Kongo: Begonnen hat alles vor gut 125 Jahren, als  der junge Hermann Wissmann Richtung Zentralafrika auszog, das  Kongobecken erforschte und Blutsbruderschaft mit dem Stamm der  Bashilange schloss. Im Jahr 2005 reiste zu den Feierlichkeiten zum 100.  Todestages zu Ehren des berühmten Afrikaforschers eine Delegation aus  dem Congo DR an und es kam die Idee auf, diese historische Beziehung  zwischen Weißenbach / Liezen und dem Kongo wiederaufleben zu lassen und  zu vertiefen. Erstes Ziel des Projekts ist es, in der Missionsstation  Mikalayi in der Kasai-Provinz eine Schule wiederherzustellen. Das  Gebäude stammt etwa aus dem Jahre 1920 und ist sehr reparaturbedürftig.  Die Stromversorgung und Unterrichtsmittel wären dann ein nächster  Schritt.</p>
<p class="visualClear"><a href="http://www.abc.cd/">www.abc.cd</a></p>

<h3>Energy for Cuba</h3>
<p><a href="efc-jpg"><img src="efc-jpg/image_mini" style="float: right; " /></a> Energy for Cuba ist ein wohltätiger Verein zur Förderung erneuerbarer  Energie in der Dritten Welt. Forschung, Studentenaustausch und  Entwicklungshilfe sind seine wesentlichen Aufgaben. Dies geschieht in  Zusammenarbeit mit der kubanischen Universidad Oriente, der Technischen  Universität (TU) Graz, der Fachhochschule Wels und der HTL Braunau.  Gegründet wurde der Verein 2002 von fünf engagierten Schülern der HTL  Braunau. Zwei Milliarden Menschen leben auf dieser Welt in Armut, der  Klimawandel wird dieses Elend noch weiter vergrößern. Wir möchten durch  Forschung- und Bildungsarbeit und Projekte im Bereich erneuerbarer  Energien in der Dritten Welt vorantreiben. Erneuerbare Energien können  den Klimawandel zwar bekämpfen, die Dritte Welt verfügt jedoch weder  über die Mittel, noch über das notwendige Know-how zur effizienten  Nutzung erneuerbarer Energieträger. Klimaschutz muss global betrieben  werden, dafür ist eine faire, weltweite Kooperation erforderlich.</p>
<p class="visualClear"><a href="http://www.energy-cuba.adm.at/">www.energy-cuba.adm.at</a></p>

<h3>Erklärung von Graz</h3>
<p><a href="evg-png"><img src="evg-png/image_mini" style="float: right; " /></a> Anfang der 70er Jahre begann eine Gruppe von GrazerInnen mit  Selbstbesteuerung für die Dritte Welt. Aus dieser Initiative entwickelte  sich die ERKLÄRUNG VON GRAZ, ein Verein für solidarische Entwicklung  mit den Ländern des Südens.<br /> Wir sind überzeugt, dass Erfolgs- und Konsumzwang dem Wert unseres  Lebens abträglich sind und setzen deshalb einen kleinen Teil unseres  Wohlstands für die Finanzierung von Projekten der autonomen Entwicklung  an einzelnen Orten in den Ländern des Südens ein.<br /> Wir wählen die von uns finanzierten Projekte selbst aus und legen großen  Wert auf einen direkten Kontakt mit den Personen, die die Projekte vor  Ort betreuen. Sie können sich auch auf unserer Homepage unter www.evg-eza.org  informieren.</p>
<p class="visualClear"><a href="http://www.evg-eza.org/">www.evg-eza.org</a></p>

<h3>Friends of Lingshed</h3>
<p><a href="fol-jpg"><img src="fol-jpg/image_mini" style="float: right; " /></a> Die Friends of Lingshed engagieren sich seit 1994 in der Region Ladakh  in Kaschmir, Nordindien. Das entlegene Dorf Lingshed ist nur über einen  mehrtägigen Marsch über 5000 Meter hohe Pässe erreichbar. Die Friends of  Lingshed finanzieren verschiedene Bildungsprojekte, um Kindern und  Jugendlichen aus Lingshed oder anderen entlegenen Dörfern in Ladakh eine  gute Schulausbildung bzw. ein Studium zu ermöglichen. Die Spendengelder  werden verwendet für Patenschaften für Schulkinder, Studentinnen und  Studenten, für das Projekt Winterunterricht (eine Art  „Nachhilfeunterricht“ in den Ferienmonaten Dezember bis Februar in  Lingshed und umliegenden Dörfern), für Umwelterziehung, für kindgerechte  Schulbücher und Unterrichtsmaterialien sowie für Berufsausbildung.  Gemeinsam mit der Dorfbevölkerung haben die Friends of Lingshed im Jahr  2000 mit Spendengeldern eine solarbeheizte Schule gebaut, die der  Grundstein für die Entwicklung eines großen Schulzentrums der örtlichen  Regierung in Lingshed war.</p>
<p class="visualClear"><a href="http://www.lingshed.org/">www.lingshed.org</a></p>

<h3>Life Earth</h3>
<p><a href="lea-jpg"><img src="lea-jpg/image_mini" style="float: right; " /></a> Der Verein Life Earth unterstützt Projekte zur Förderung in den  Bereichen Bildung, Gesundheit und Soziales in Ostafrika. Dies sind  Photovoltaik- und Solarheißwasserprojekte für Spitäler,  Gesundheitszentren und „Dorfkliniken“, Patenkind-Aktionen für  AIDS-Waisen sowie soziale Projekte zur Unterstützung in Slumgebieten und  Aufklärungsprojekte. Derzeit läuft das Gesundheitsförderungsprojekt  „Sehen ohne Grenzen“ in Kooperation mit Augenärzten des LKH Bruck/Mur in  Tansania und für 2010 ist die Initiierung eines Projekts mit jungen  Prostituierten in Uganda geplant. In den Radio-Sendungen im Februar  informiert Life Earth über diverse sozial- und gesundheitskritische  Probleme in Tansania und Uganda und darüber wie die oben erwähnten  Projekte des Vereins auf diese Probleme reagieren.</p>
<p class="visualClear"><a href="http://www.lifeearth.at/">www.lifeearth.at</a></p>

<h3>Mojo</h3>
<p><a href="mojo_johannesburg-jpg"><img src="mojo_johannesburg-jpg/image_mini" style="float: right; " /></a> Das Projekt 2010: 15 Studierende der Fachrichtungen Architektur und  Bauingenierwesen der TU Graz und der TU Wien planen und bauen eine  Schule an der Wild Coast in Südafrika. Der Standort liegt in einer der  ärmsten Regionen Südafrikas, dem ehemaligen Transkei. Es wird ein  genereller Masterplan für das Schulareal entworfen, welcher für die  nächsten 10 Jahre konzipiert ist. Im Sommer 2010 werden die ersten  Gebäude - Klassenräume für die Pre School und die Primary School - von  den Studierenden errichtet. Die Eröffnung ist für Jänner 2011 geplant.  Unterrichtet werden Kinder aus der Region für die der Besuch unserer  Schule kostenlos ist. Somit bekommen auch ärmere Familien die  Gelegenheit, ihren Kindern eine schulische Ausbildung zu ermöglichen.</p>
<p>M O J O - hinter diesem Kürzel verbirgt sich ein gemeinnütziger  Verein, der sich zum Ziel gesetzt hat, Studierenden von den Fakultäten  Architektur und Bauingenieurwesen eine praxisnahe Ausbildung im Rahmen  von Fullscale Projekten zu ermöglichen. Weiters wird im Rahmen von MOJO  der Austausch von Wissen, praktischem Können und kulturellen Erfahrungen  zwischen Europa und Afrika gefördert.</p>
<p class="visualClear"><a href="http://www.ithuba-mojo.net/">www.ithuba-mojo.net</a></p>

<h3>NIcaúnidAT</h3>
<p><a href="nic-jpg"><img src="nic-jpg/image_mini" style="float: right; " /></a> Der Verein NIcaúnidAT realisiert und plant Projekte in Granada,  Nicaragua mit Unterstützung von Pan y Arte Österreich. NIcaúnidAT, ein  Verein von Studentinnen der Universität für angewandte Kunst Wien,  arbeitet anhand der Medien Fotografie, Video und Sound mit Jugendlichen  zum Thema „Tourismus“.<br /> In der ersten Sendung (Deutsch/Spanisch) erzählt die Initiatorin Jasmin  Schaitl, wie es zum Projekt Asomate kam. Darin realisierten die  Jugendlichen Kurzfilme zum Thema der sexuellen Ausbeutung. Außerdem  führten sie unterschiedlichste Interviews auf der Straße, mit der  Polizei, dem Bürgermeister, usw. durch. Das Ziel war, die Jugendlichen  über die Kunst zur Reflexion ihres Alltags zu bewegen, im Speziellen die  sexuelle Gewalt und Effekte des Tourismus wahrzunehmen.<br /> In der zweiten Sendung wandern wir akustisch durch Nicaragua! Stationen  der Reise: die Tourismusstadt Granada, das Festival de Poesia und  Gioconda Belli, die Vulkaninsel Ometepe, ein Jugendtheaterstück, bis ins  stille Naturreservat Tisey-Estanzuela in Esteli.</p>
<p class="visualClear"><a href="http://nicaunidat.wordpress.com/">nicaunidat.wordpress.com</a><br /> <a href="http://www.panyarte.at/">www.panyarte.at</a></p>

<h3>Tifinagh</h3>
<p><a href="tif-jpg"><img src="tif-jpg/image_mini" style="float: right; " /></a> Der Verein Tifinagh unterstützt die Tuareg- Kel Tifinagh im Raum Agadez  und Aïr. Alle Mitglieder des Vereines bereisen das Gebiet laufend und  haben persönlichen Kontakt zu den Tuareg in Städten, Dörfern und vor  allem in den Nomadengebieten. Der Verein IZAT in Agadez ist  Kooperationspartner, seine Ziele sind die Verwirklichung nachhaltiger  Entwicklungsprojekte und eine Verbesserung der Schul- und  Berufsausbildung. Sendung I: Die Sendung gibt Einblick in die  Lebenssituation der Tuareg(nomaden) in Niger und erzählt vom Versuch  einiger Reisender, durch den Verein Tifinagh, Unterstützung zu bieten.<br /> Sendung II: Ishumar-Guitar – oder Wüstenrock. Ein Abriss zur Entwicklung  dieses Musikstils – besonders geprägt durch Tinariwen oder Abdallah  Ouambadougou. Eine musikalische Reise durch die Wüste.</p>
<p class="visualClear"><a href="http://vereintifinagh.blogspot.com/">vereintifinagh.blogspot.com</a></p>

<h3>Zikomo</h3>
<p><a href="zikomo_sambia-jpg"><img src="zikomo_sambia-jpg/image_mini" style="float: right; " /></a> ZIKOMO ist ein Verein zur Förderung afrikanischer Studenten und  Studentinnen in ihren Heimatländern mit dem Sitz in Graz (Österreich).  Der Verein bezweckt die Akquirierung von Spendengeldern, die  ausschließlich für die Ausbildung von afrikanischen Studentinnen und  Studenten in ihren Heimatländern verwendet werden, wobei sich die  Aktivitäten zurzeit auf Sambia konzentrieren.</p>
<ul>
<li>68% der sambischen Bevölkerung leben unter der Armutsgrenze und  verdienen weniger als 1 Euro pro Tag. Über 50% der Menschen sind  arbeitslos. Die durchschnittliche Lebenserwartung liegt bei 38 Jahren.</li>
<li>Eine Ausbildung vor Ort reduziert das Risiko permanenter Armut um 76%.</li>
<li>Durch Steigerung des Ausbildungsniveaus der Menschen vor Ort wächst  das Potential an qualifizierten und eigenständigen Lösungen durch die  hervorgebrachten Fachkräfte.</li>
<li>Die Absolventinnen und Absolventen unseres Förderprogramms tragen  zur Entwicklung ihrer Heimatländer bei und können die Lebensbedingungen  für ihre Mitmenschen vor Ort langfristig verbessern.</li>
</ul>
Durch Ihre Unterstützung können SIE einen Stein ins Rollen bringen, gemeinsam versetzen wir Berge!
<p class="visualClear"><a href="http://www.zikomo.at/">www.zikomo.at</a></p>

<h2>Der Verein Radio Helsinki</h2>
<p>Der Verein Radio Helsinki: In Österreich gibt es aktuell 13 Freie Radios. Seit dem Jahr 2000 sendet Radio Helsinki im Großraum Graz und im Internet 24 Stunden täglich! Radio ist öffentlicher Raum. Öffentlicher Raum darf nicht ausschließlich von Ökonomie bestimmt werden. Frei ist dieses Radio, weil keine Einzelpersonen über den Programminhalt bestimmen, sondern die ProduzentInnen selbst entscheiden, worüber und wie sie ihre Sendezeit gestalten. Zwei wesentliche Grundsätze bestimmen Freies Radio: Nichtkommerzialität und Offener Zugang. Ersteres gewährleistet Unabhängigkeit in der Sendungsgestaltung. Zweiteres garantiert Meinungsvielfalt, weil prinzipielle jedeR Programm gestalten kann: über Selbstrepräsentation den öffentlichen Raum gestaltet. <a href="http://www.helsinki.at/">www.helsinki.at</a></p>

<h2>* "Cocoyoc"...</h2>
<ul>
<li>...Nahuatl: "ein Ort, wo sich die Kojoten treffen...",  bezeichnet im 11.Jh. einen voraztekischen Ort in Mexiko (heute im  Bundesstaat Morelos).</li>
<li>...Hernan Corteś: der Konquistador zog 1521 durch nämlichen Ort und steht für den "Beginn" kolonialer-europäischer Landnahme.</li>
<li>...Ivan Illich und Paolo Freire: hatten ab 1960 nahe Cocoyoc in Cuernavaca ihr Centro Intercultural de Documentación.</li>
<li>...Baraba Ward: Verfasste 1974 die "Cocoyoc Deklaration" für eine  UNO Konferenz, die Entwicklung gegen das Wachstumsparadigma, staatliche  Programmatiken, sondern von "unten" definieren sollte.</li>
</ul>
<p>..."Cocoyoc"  - verweist auf die Mehrdeutigkeit kolonialer  Verfassungen... von denen wir ausgehen... Entwicklungspolitik  korrespondiert genauso mehrdeutig mit globalen Disparitäten... ob im  "global Village" oder "urban Globe"...</p>

<p><a href="http://www.fairstyria.at/"><img src="fairstyria-jpg/image_mini" /></a></p>
             """},
        'childs': [
{'type':'File', 'title': u'abschlussbericht_eza_stmk_land_web.pdf', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/abschlussbericht_eza_stmk_land_web.pdf')}},
{'type': 'Image', 'title': u'bik.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/bik.jpg')}},
{'type': 'Image', 'title': u'efc.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/efc.jpg')}},
{'type': 'Image', 'title': u'evg.png', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/evg.png')}},
{'type': 'Image', 'title': u'fairstyria.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/fairstyria.jpg')}},
{'type': 'Image', 'title': u'fairstyria.png', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/fairstyria.png')}},
{'type': 'Image', 'title': u'fol.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/fol.jpg')}},
{'type': 'Image', 'title': u'lea.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/lea.jpg')}},
{'type': 'Image', 'title': u'mojo_johannesburg.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/mojo_johannesburg.jpg')}},
{'type': 'Image', 'title': u'nic.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/nic.jpg')}},
{'type': 'Image', 'title': u'tif.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/tif.jpg')}},
{'type': 'Image', 'title': u'zikomo_sambia.jpg', 'data':{'image':sht.load_file(globals(), 'data/cocoyoc/zikomo_sambia.jpg')}},
                ]
             },

             ]
    sht.create_item_runner(ctx, content_structure, lang='de', logger=logger)

    #livestream
    ctx = site['livestream']
    content_structure = [
        {'type': 'File', 'title': u'live128mp3.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live128mp3.m3u')}},
        {'type': 'File', 'title': u'live128mp3.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live128mp3.pls')}},
        {'type': 'File', 'title': u'live128ogg.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live128ogg.m3u')}},
        {'type': 'File', 'title': u'live128ogg.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live128ogg.pls')}},
        {'type': 'File', 'title': u'live160mp3.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live160mp3.m3u')}},
        {'type': 'File', 'title': u'live160mp3.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live160mp3.pls')}},
        {'type': 'File', 'title': u'live160ogg.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live160ogg.m3u')}},
        {'type': 'File', 'title': u'live160ogg.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live160ogg.pls')}},
        {'type': 'File', 'title': u'live96mp3.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live96mp3.m3u')}},
        {'type': 'File', 'title': u'live96mp3.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live96mp3.pls')}},
        {'type': 'File', 'title': u'live96ogg.m3u', 'data':{'file':sht.load_file(globals(), 'data/livestream/live96ogg.m3u')}},
        {'type': 'File', 'title': u'live96ogg.pls', 'data':{'file':sht.load_file(globals(), 'data/livestream/live96ogg.pls')}},
    ]
    sht.create_item_runner(ctx, content_structure, lang='de', logger=logger)


LIVESTREAM_DESC = u"""Radio hören im Internet."""
LIVESTREAM_TEXT = u"""<div class="autoFlowPlayer audio"><a class="external-link" href="http://live.helsinki.at:8088/live160.mp3">http://live.helsinki.at:8088/live160.mp3</a></div>
<h3>Livestream Playlisten im Ogg/Vorbis Format</h3>
<p>Hohe Qualität, 160 kpbs: <a class="internal-link" href="live160ogg-m3u"><span class="internal-link">m3u</span></a> / <a class="internal-link" href="live160ogg-pls">pls</a><br />Mittlere Qualität, 128 kpbs: <a class="internal-link" href="live128ogg-m3u">m3u</a> / <a class="internal-link" href="live128ogg-pls">pls</a><br />Niedriege Qualität, 96 kbps: <a class="internal-link" href="live96ogg-m3u">m3u</a> / <a class="internal-link" href="live96ogg-pls">pls</a></p>
<h3>Livestream Playlisten im MP3 Format</h3>
<p>Hohe Qualität, 160 kpbs: <a class="internal-link" href="live160mp3-m3u">m3u</a> / <a class="internal-link" href="live160mp3-pls">pls</a><br />Mittlere Qualität, 128 kpbs: <a class="internal-link" href="live128mp3-m3u">m3u</a> / <a class="internal-link" href="live128mp3-pls">pls</a><br />Niedriege Qualität, 96 kbps: <a class="internal-link" href="live96mp3-m3u">m3u</a> / <a class="internal-link" href="live96mp3-pls">pls</a></p>
<h3>Die direkten Streamadressen im Ogg/Vorbis Format</h3>
<p><a class="external-link" href="http://live.helsinki.at:8088/live160.ogg">http://live.helsinki.at:8088/live160.ogg</a><br /><a class="external-link" href="http://live.helsinki.at:8088/live128.ogg">http://live.helsinki.at:8088/live128.ogg</a><br /><a class="external-link" href="http://live.helsinki.at:8088/live96.ogg">http://live.helsinki.at:8088/live96.ogg</a></p>
<h3>Die direkten Streamadressen im MP3 Format</h3>
<p><a class="external-link" href="http://live.helsinki.at:8088/live160.mp3">http://live.helsinki.at:8088/live160.mp3</a><br /><a class="external-link" href="http://live.helsinki.at:8088/live128.mp3">http://live.helsinki.at:8088/live128.mp3</a><br /><a class="external-link" href="http://live.helsinki.at:8088/live96.mp3">http://live.helsinki.at:8088/live96.mp3</a></p>
<h3>Programme, die OGG Vorbis-Streams abspielen können</h3>
<p><a class="external-link" href="http://www.videolan.org/vlc/">VideoLAN</a> (Liunx, Windows, Mac OS X)<br /><a class="external-link" href="http://www.rhythmbox.org">Rhythmbox</a> (Linux)<br /><a class="external-link" href="http://www.winamp.com">WinAmp</a> (Windows)</p>
"""

KONTAKT_TEXT = u"""
<h2>Radio Helsinki - Verein Freies Radio Steiermark</h2>
<p>Griesgasse 8, 8020 Graz<br />
Tel: + 43 316 830 880 (Sendestudio: Durchwahl 80)<br />
Fax: + 43 316 830 880 84</p>
<p><b>Büro:</b> <a class="mail-link" href="mailto:office@helsinki.at">office@helsinki.at</a><br />
<b>Programmrat:</b> <a class="mail-link" href="mailto:programmrat@helsinki.at">programmrat@helsinki.at</a><br />
<b>Technik:</b> <a class="mail-link" href="mailto:technik@helsinki.at">technik@helsinki.at</a><br />
<b>Vorstand:</b> <a class="mail-link" href="mailto:vorstand@helsinki.at">vorstand@helsinki.at</a><br />
<b>Musikredaktion:</b> <a class="mail-link" href="mailto:musikredaktion@helsinki.at">musikredaktion@helsinki.at</a><br />
<b>Workshops:</b> <a class="mail-link" href="mailto:office@helsinki.at">office@helsinki.at</a><br /></p>
"""

CHARTA_TEXT = u"""
<p><b>I. Grundsätze des <a class="external-link" href="http://www.freie-radios.at/">Verbandes Freier Radios Österreich</a></b></p>
<p>Freie Radios sind unabhängige, gemeinnützige, nicht-kommerzielle  und auf kommunikativen Mehrwert ausgerichtete Organisationen, die einen  allgemeinen und freien Zugang zu Sendeflächen für Rundfunkverstaltungen  bereitstellen, um die freie Meinungsäußerung zu fördern. Als dritte  Säule der Rundfunklandschaft neben öffentlicht-rechtlichen und  kommmerziell-privaten RundfunkveranstalterInnen erweitern Freie Radios  die Meinungsvielfalt.</p>
<p><b>Offener Zugang / Public Access</b></p>
<p>Freie Radios geben allen Personen und Gruppen innerhalb des  gesetzlichen Rahmens die Möglichkeit zur unzensierten Meinungsäußerung  und Informationsvermittlung. Vorrang haben dabei soziale, kulturelle und  ethnische Minderheiten sowie solche Personen und Gruppen, die wegen  ihrer gesellschaftlichen Marginalisierung oder sexistischen oder  rassistischen Diskriminierung in den Medien kaum oder nicht zu Wort kommen.</p>
<p><b>Partizipation</b></p>
<p>Freie Radios stellen Trainings-, Produktions- und  Verteilungsmöglichkeiten zur Verfügung. Sie bilden Plattformen lokaler  und (über-)regionaler Musik-, Kunst- und Kulturproduktion für  gesellschaftspolitische Initiativen und für gesellschaftlich oder medial  marginalisierte Communities. Sie laden ihre HörerInnen zur aktiven  Beteiligung ein, spiegeln die gesellschaftliche, kulturelle und  sprachliche Vielfalt ihrer Ausstrahlungsgebiete wider und fördern den  interkulturellen Dialog.</p>
<p><b>Gemeinnützigkeit / Nichtkommerzialität</b></p>
<p>Freie Radios sind kein Privateigentum eines/r Einzelnen, sondern  sind gemeinsam von ihren NutzerInnen getragene Organisationsformen, die  vor allem dem Prinzip der Gemeinnützigkeit unterliegen. Ihre Tätigkeit  ist nicht auf Gewinn ausgerichtet und verfolgt das Prinzip eines  werbefreien Radios ohne kommerzielle Produktwerbung. Um die Existenz und  Unabhängigkeit gewährleisten zu können, braucht es eine Diversifizierung der  Einnahmequellen. Die Finanzierung erfolgt durch Eigenleistungen wie  Projekte oder Kooperationen, öffentliche Förderungen, Mitgliedsbeiträge  und Spenden oder auch Sponsoring.</p>
<p><b>Transparenz / Organisation</b></p>
<p>In Freien Radios sind die Organisation und die Auswahlkriterien  für Sendeinhalte durchschaubar und nachprüfbar zu halten. Die  TrägerInnen Freier Radios handhaben ihr Management, ihre  Programmgestaltung und ihre Beschäftigungspraxis so, dass sie jede Form  der Diskriminierung ausschließt; sie sind dabei gegenüber allen  UnterstützerInnen, dem Personal und den ehrenamtlichen MitarbeiterInnen offen und verantwortlich. Sie fördern  die Mitwirkung von MigrantInnen und Frauen in allen Bereichen.</p>
<p><b>Lokalbezug</b></p>
<p>Freie Radios verstehen sich als Kommunikationsmittel im lokalen  und regionalen Raum und unterstützen die regionale Entwicklung. Damit  fungieren freie Radios auch als fördernde Plattformen für  regionalbezogene Kunst- und Kulturschaffende, in denen es für  KünstlerInnen Auftritts- und Verbreitungsmöglichkeiten gibt. Darüber  hinaus findet eine Auseinandersetzung mit überregionalen und  internationalen Themen statt. Freie Radios arbeiten aktiv zusammen, z.B. durch Programmaustausch oder  die gemeinsame Realisierung von medialen, kulturellen, künstlerischen  oder gesellschaftspolitischen Projekten.</p>
<p><b>Unabhängigkeit</b></p>
<p>Freie Radios sind im Besitz, in der Organisationsform, in der  Herausgabe und in der Programmgestaltung unabhängig von staatlichen,  kommerziellen und religiösen Institutionen und politischen Parteien.</p>
<p><b>Anspruch</b></p>
<p>Freie Radios fördern eine selbstbestimmte, solidarische und  emanzipatorische Gesellschaft. Sie wenden sich gegen jede Form der  Diskriminierung aufgrund von Geschlecht oder sexueller Orientierung,  Herkunft, Abstammung Hautfarbe oder Ethnie, religiöser oder politischer  Anschauung, aufgrund körperlicher oder geistiger Fähigkeiten, sozialer  Herkunft, Sprache oder Alter. Sie treten für freie Meinungsäußerung,  Meinungsvielfalt, Gleichberechtigung, Menschenwürde und Demokratie ein.</p>
<p><br /> <b>II. Forderungen des Verbandes Freier Radios Österreich</b></p>
<p><b>Gesetzliche Anerkennung</b></p>
<p>Aufgrund ihrer Leistungen im öffentlichen Interesse müssen Freie  Radios im Privatradiogesetz und KommAustria-Gesetz als eigene Kategorie  anerkannt werden. Diese Leistungen sind insbesondere der Offene Zugang  zu Sendeflächen im Rundfunk, die publizistische Ergänzung im lokalen und  regionalen Bereich sowie die Vermittlung von Medienkompetenz.</p>
<p><b>Freie-Radios-Fonds</b></p>
<p>Die Leistungen im öffentlichen Interesse, die die Freien Radios  erfüllen, müssen öffentlich gefördert werden. Die Freien Radios fordern  die Einrichtung eines "Freie-Radios-Fonds", der aus jenem Teil der  Rundfunkgebühren gespeist wird, der nicht dem ORF zufließt  ("Gebührensplitting"). Bezüglich der urheberrechtlichen Abgaben genießen  Freie Radios einen Sonderstatus, der ihrem gemeinnützigen Charakter  entspricht.</p>
<p><b>Triales Rundfunksystem und BeauftragteR für Freie Medien</b></p>
<p>Die Dreiteilung des Rundfunksystems in öffentlich-rechtliche,  privat- kommerzielle und gemeinnützige Freie Rundfunkveranstalter  (triales Rundfunksystem) muss sich (strukturell in der Konstruktion) in  der Struktur der Medienbehörde sowie bei der Lizenzvergabe  widerspiegeln. In Sendegebieten, wo Bedarf vorhanden ist, muss die  Versorgung mit Freiem Radio durch Vorrang bei der Lizenzvergabe  gewährleistet sein. Als AnsprechpartnerIn für Forschung und Entwicklung  im Dritten Rundfunksektor muss in der Medienbehörde einE BeauftragteR  für Freie Medien installiert werden. Die Medienforschung muss künftig  verstärkt auf die gesellschaftlichen Leistungen zugangsoffener Freier  Radios eingehen.</p>
<p><b>Journalistische Gleichberechtigung</b></p>
<p>MitarbeiterInnen Freier Radios sind frei in ihrer Recherche und sind JournalistInnen anderer Medien gleichgestellt.</p>
<p><b>Mitbestimmung und Stellungnahme</b></p>
<p>Bei Erarbeitung von Gesetzen, Gesetzesänderungen und  internationalen Verträgen, die das Medien- und Fernmeldewesen betreffen,  haben die VertreterInnen der Freien Radios das Recht auf Mitbestimmung  und Stellungnahme.</p>
"""
