-- https://dbdiagram.io/d/5e84a1494495b02c3b8918bd

CREATE TABLE "references" (
  "uuid" varchar PRIMARY KEY,
  "source" varchar,
  "source_id" varchar,
  "first_fetched" timestamp,
  "last_fetched" timestamp,
  "last_modified" timestamp,
  "hash" varchar,
  "data" jsonb
);

CREATE TABLE "sources" (
  "id" varchar PRIMARY KEY,
  "name" varchar,
  "ranking" float
);

CREATE TABLE "collections" (
  "uuid" varchar PRIMARY KEY,
  "name" varchar,
  "created" timestamp,
  "last_modified" timestamp,
  "data" jsonb
);

CREATE TABLE "collections_references" (
  "collection_uuid" varchar,
  "reference_uuid" varchar,
  "data" jsonb,
  PRIMARY KEY ("collection_uuid", "reference_uuid")
);

ALTER TABLE "references" ADD FOREIGN KEY ("source") REFERENCES "sources" ("id");

ALTER TABLE "collections_references" ADD FOREIGN KEY ("collection_uuid") REFERENCES "collections" ("uuid");

ALTER TABLE "collections_references" ADD FOREIGN KEY ("reference_uuid") REFERENCES "references" ("uuid");


-- add test data
INSERT INTO "sources" VALUES ('Test', 'Test', 1);
INSERT INTO "references" VALUES ('1','Test','Dummy-Id',now(),now(),now(),'xyz','{ "ranking":1, "fulltext":"Die Erde bewegt sich in einer elliptischen Umlaufbahn um die Sonne, so dass es dem Abstand entsprechend zu zyklischen Schwankungen des Erdklimas kommt. Welchen Einfluss hat die Sonne auf den heutigen Klimawandel? Nutzungsbedingungen Das urheberrechtlich geschützte Werk auf dieser Seite kann auf Grund der Creative Commons-Lizenz CC BY 4.0 ( https://creativecommons.org/licenses/by/4.0/deed.de ) kostenfrei genutzt werden. Alle Fotos und Videos können nur unter Einhaltung der Lizenzbestimmungen vervielfältigt, weitergegeben und verändert werden. Die Lizenzbestimmungen finden sich unter: https://creativecommons.org/licenses/by/4.0/deed.de . Insbesondere sind zur Einhaltung der Lizenzbestimmungen und zur Wahrung der Urheberpersönlichkeitsrechte: 1. die Urheber der genutzten Werke zu nennen; 2. ggf. Veränderungen - unter Beachtung der Urheberpersönlichkeitsrechte - des Werkes anzugeben und alle vorherigen Änderungsangaben beizubehalten; 3. ein Hinweis auf die Lizenzbestimmungen in angemessener Form (Text, URL oder Hyperlink) aufzunehmen sowie das Werk mit dem CC-Icon zu kennzeichnen; 4. den Eindruck zu vermeiden, dass Ihre Nutzung vom Urheber bzw. ZDF unterstützt wird. Die unwiderrufliche Lizenz endet mit Ablauf der gesetzlichen Schutzfristen oder vorzeitig, wenn die Lizenzbestimmungen nicht eingehalten werden. Bei Verwendung immer nennen: ZDF/Terra X/Gruppe 5/Luise Wagner, Jonas Sichert, Rudi Kirschen Der Video-Clip entstand in Zusammenarbeit mit Meteorologe Prof. Dr. Stephan Borrmann, Professor der Johannes Gutenberg-Universität Mainz und Wissenschaftliches Mitglied am Max-Planck-Institut für Chemie sowie dem Klimawissenschatftler Dr. Dirk Notz. Dieser leitet am Max-Planck-Institut für Meteorologie in Hamburg seit 2008 die Forschungsgruppe", "source":{ "id":"SODIS", "name":"Sodis Content Pool", "total_count": 5000, "ranking":1 }, "lom":{ "general":{ "identifier":"xyz", "title":"Klimafaktor Sonne", "language":"de", "keyword":["Sonne", "Erwärmung", "Klima"] }, "educational": { "intendedEndUserRole":["learner","teacher"], "context":["compulsory education","lower secondary school","upper secondary school"], "context_de_DE":["compulsory education","lower secondary school","upper secondary school"], "typicalAgeRange":{"from":10, "to":18} } } }');
INSERT INTO "collections" VALUES ('1', 'Beispielsammlung', null);
INSERT INTO "collections_references" VALUES('1','1', null);