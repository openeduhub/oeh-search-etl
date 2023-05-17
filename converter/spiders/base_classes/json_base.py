# base for spiders using local 'json' data and need to access them
class JSONBase:
    json = None

    def get(self, *params, mode="first", json=None):
        if json == None:
            json = self.json

        for param in params:
            value = json
            for key in param.split("."):
                if value:
                    value = value.get(key)
                else:
                    return None
            if value is not None:
                return value
        return None


if __name__ == '__main__':
    data = {
        "parse": {
            "title": "Dogme",
            "pageid": 238,
            "revid": 22135,
            "text": {
                "*": "<div class=\"mw-parser-output\"><p>... ist ein kommunikativer Ansatz des Sprachenlehrens, der dazu auffordert, auf den Einsatz von Lehrbüchern zu verzichten und stattdessen auf kommunikativen Austausch zwischen Schülern und Lehrern zu setzen.\n</p><p>Der Dogme-Ansatz hat zehn Hauptprinzipien:<sup id=\"cite_ref-1\" class=\"reference\"><a href=\"#cite_note-1\">&#91;1&#93;</a></sup>\n</p>\n<ol><li><b>Interaktivität</b>: der direkte Weg zum Lernen ist in der Interaktivität zwischen Lehrern und Schülern sowie zwischen den Schülern selbst zu finden.</li>\n<li><b>Einbindung</b>: Schüler sind beim Lernprozess besonders engagiert, wenn es dabei um Inhalte geht, die sie selbst kreiert haben.</li>\n<li><b>Dialogische Prozesse</b>: Lernen wird als sozialer und dialogischer Prozess verstanden, in dem Wissen gemeinschaftlich aufgebaut wird.</li>\n<li><b>Ko-Konstruktion (des Lernens)</b>: Lernen findet durch Konversation statt, in denen Lernender und Lehrer Wissen und Fähigkeiten gemeinsam hervorbringen.</li>\n<li><b>Entstehung</b>: Sprache und Grammatik entstehen aus dem Lernprozess heraus. Darin liegt ein klarer Unterschied zu der Vorstellung, die Lerner würden sich eine bereits existierende Sprache \"aneignen\".</li>\n<li><b>Angebotscharakter</b>: die Rolle des Lehrers besteht darin, den Angebotscharakter des Sprachenlernens dadurch zu optimieren, dass er die Aufmerksamkeit auf entstehende Sprache richtet.</li>\n<li><b>Stimme</b>: Der Stimme des Lernenden, seinen Überzeugungen und seinem Wissen wird Anerkennung entgegengebracht.</li>\n<li><b>Empowerment</b>: Die Verbannung von professionell publizierten Materialien und Lehrbüchern aus dem Klassenzimmer stellt eine Ermächtigung der Schüler und Lehrer zu eigenständigem Lehr- und Lernhandeln dar.</li>\n<li><b>Relevanz</b>: verwendete Materialien (z. B. Texte, Tondokumente und Videos) sollen für die Lernenden relevant sein.</li>\n<li><b>Kritischer Gebrauch</b>: Lehrer und Schüler sollen mit professionell publizierten Materialien und Lehrbüchern in einer kritischen Weise umgehen, die berücksichtigt, dass solche Materialien kulturelle und ideologische Einfärbungen und Voreingenommenheiten beinhalten (können).</li></ol>\n<h2><span class=\"mw-headline\" id=\"Links\">Links</span><span class=\"mw-editsection\"><span class=\"mw-editsection-bracket\">[</span><a href=\"/index.php?title=Dogme&amp;veaction=edit&amp;section=1\" class=\"mw-editsection-visualeditor\" title=\"Abschnitt bearbeiten: Links\">Bearbeiten</a><span class=\"mw-editsection-divider\"> | </span><a href=\"/index.php?title=Dogme&amp;action=edit&amp;section=1\" title=\"Abschnitt bearbeiten: Links\">Quelltext bearbeiten</a><span class=\"mw-editsection-bracket\">]</span></span></h2>\n<ul><li><a rel=\"nofollow\" class=\"external free\" href=\"https://de.wikipedia.org/wiki/Dogme\">https://de.wikipedia.org/wiki/Dogme</a><div class=\"mw-references-wrap\"><ol class=\"references\"></ol></div></li></ul>\n<li id=\"cite_note-1\"><span class=\"mw-cite-backlink\"><a href=\"#cite_ref-1\">↑</a></span> <span class=\"reference-text\"><a rel=\"nofollow\" class=\"external free\" href=\"https://de.wikipedia.org/wiki/Dogme\">https://de.wikipedia.org/wiki/Dogme</a></span>\n</li>\n\n\n<!-- \nNewPP limit report\nCached time: 20210201125246\nCache expiry: 86400\nDynamic content: false\nCPU time usage: 0.035 seconds\nReal time usage: 0.036 seconds\nPreprocessor visited node count: 19/1000000\nPreprocessor generated node count: 46/1000000\nPost‐expand include size: 0/2097152 bytes\nTemplate argument size: 0/2097152 bytes\nHighest expansion depth: 2/40\nExpensive parser function count: 0/100\nUnstrip recursion depth: 0/20\nUnstrip post‐expand size: 83/5000000 bytes\n-->\n<!--\nTransclusion expansion time report (%,ms,calls,template)\n100.00%    0.000      1 -total\n-->\n\n<!-- Saved in parser cache with key da_zum_de:pcache:idhash:238-0!canonical and timestamp 20210201125246 and revision id 22135\n -->\n</div>"
            },
            "langlinks": [],
            "categories": [
                {
                    "sortkey": "",
                    "*": "DaF-Glossar"
                }
            ],
            "links": [],
            "templates": [],
            "images": [],
            "externallinks": [
                "https://de.wikipedia.org/wiki/Dogme"
            ],
            "sections": [
                {
                    "toclevel": 1,
                    "level": "2",
                    "line": "Links",
                    "number": "1",
                    "index": "1",
                    "fromtitle": "Dogme",
                    "byteoffset": 2008,
                    "anchor": "Links"
                }
            ],
            "parsewarnings": [],
            "displaytitle": "Dogme",
            "iwlinks": [],
            "properties": [
                {
                    "name": "description",
                    "*": "... ist ein kommunikativer Ansatz des Sprachenlehrens, der dazu auffordert, auf den Einsatz von Lehrbüchern zu verzichten und stattdessen auf kommunikativen Austausch zwischen Schülern und Lehrern zu setzen."
                }
            ]
        }
    }

    j = JSONBase()
    j.json = data
    props = j.get("parse.properties")
    if props:
        description = list(
            map(
                lambda x: x["*"],
                filter(lambda x: x["name"] == "description", props),
            )
        )
    print(description)
