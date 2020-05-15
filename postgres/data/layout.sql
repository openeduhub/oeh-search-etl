-- 
CREATE TABLE "references" (
  "uuid" varchar PRIMARY KEY,
  "enabled" boolean,
  "last_updated" timestamp
);

CREATE TABLE "sources" (
  "id" varchar PRIMARY KEY,
  "type" integer,
  "name" varchar,
  "url" varchar,
  "ranking" float
);

CREATE TABLE "collections" (
  "uuid" varchar PRIMARY KEY,
  "name" varchar,
  "created" timestamp,
  "last_updated" timestamp,
  "data" jsonb
);

CREATE TABLE "collections_references" (
  "collection_uuid" varchar,
  "reference_uuid" varchar,
  "last_updated" timestamp,
  "data" jsonb,
  PRIMARY KEY ("collection_uuid", "reference_uuid")
);

CREATE TABLE "references_metadata" (
  "source" varchar,
  "source_id" varchar,
  "uuid" varchar,
  "hash" varchar,
  "last_seen" timestamp,
  "last_updated" timestamp,
  "data" jsonb,
  PRIMARY KEY ("source", "source_id")
);

-- ALTER TABLE "sources" ADD FOREIGN KEY ("id") REFERENCES "references_metadata" ("source");

-- ALTER TABLE "references" ADD FOREIGN KEY ("uuid") REFERENCES "references_metadata" ("uuid");

-- ALTER TABLE "collections" ADD FOREIGN KEY ("uuid") REFERENCES "collections_references" ("collection_uuid");

-- ALTER TABLE "references" ADD FOREIGN KEY ("uuid") REFERENCES "collections_references" ("reference_uuid");


-- add test data
-- INSERT INTO "sources" VALUES ('Test', 'Test', 1);
-- INSERT INTO "references" VALUES ('1','Test','Dummy-Id',now(),now(),now(),'xyz','{ "ranking":1, "fulltext":"Die Erde bewegt sich in einer elliptischen Umlaufbahn um die Sonne, so dass es dem Abstand entsprechend zu zyklischen Schwankungen des Erdklimas kommt. Welchen Einfluss hat die Sonne auf den heutigen Klimawandel? Nutzungsbedingungen Das urheberrechtlich geschützte Werk auf dieser Seite kann auf Grund der Creative Commons-Lizenz CC BY 4.0 ( https://creativecommons.org/licenses/by/4.0/deed.de ) kostenfrei genutzt werden. Alle Fotos und Videos können nur unter Einhaltung der Lizenzbestimmungen vervielfältigt, weitergegeben und verändert werden. Die Lizenzbestimmungen finden sich unter: https://creativecommons.org/licenses/by/4.0/deed.de . Insbesondere sind zur Einhaltung der Lizenzbestimmungen und zur Wahrung der Urheberpersönlichkeitsrechte: 1. die Urheber der genutzten Werke zu nennen; 2. ggf. Veränderungen - unter Beachtung der Urheberpersönlichkeitsrechte - des Werkes anzugeben und alle vorherigen Änderungsangaben beizubehalten; 3. ein Hinweis auf die Lizenzbestimmungen in angemessener Form (Text, URL oder Hyperlink) aufzunehmen sowie das Werk mit dem CC-Icon zu kennzeichnen; 4. den Eindruck zu vermeiden, dass Ihre Nutzung vom Urheber bzw. ZDF unterstützt wird. Die unwiderrufliche Lizenz endet mit Ablauf der gesetzlichen Schutzfristen oder vorzeitig, wenn die Lizenzbestimmungen nicht eingehalten werden. Bei Verwendung immer nennen: ZDF/Terra X/Gruppe 5/Luise Wagner, Jonas Sichert, Rudi Kirschen Der Video-Clip entstand in Zusammenarbeit mit Meteorologe Prof. Dr. Stephan Borrmann, Professor der Johannes Gutenberg-Universität Mainz und Wissenschaftliches Mitglied am Max-Planck-Institut für Chemie sowie dem Klimawissenschatftler Dr. Dirk Notz. Dieser leitet am Max-Planck-Institut für Meteorologie in Hamburg seit 2008 die Forschungsgruppe", "lom":{ "general":{ "identifier":"xyz", "title":"Klimafaktor Sonne", "language":"de", "keyword":["Sonne", "Erwärmung", "Klima"] }, "technical": { "location" : "http://wirlernenonline.de" }, "educational": { "intendedEndUserRole":["learner","teacher"], "context":["compulsory education","lower secondary school","upper secondary school"], "context_de_DE":["compulsory education","lower secondary school","upper secondary school"], "typicalAgeRange":{"from":10, "to":18} } } }');
INSERT INTO "collections" VALUES ('EDITORIAL', 'Empfehlungen der Redaktion', now(), now(), '{ "editorial": true }');
INSERT INTO "collections" VALUES ('FEATURED', 'Startseite / Gefeatured', now(), now(), '{ "featured": true }');
-- INSERT INTO "collections_references" VALUES('1','1', null);https://dbdiagram.io/d/5e84a1494495b02c3b8918bd

-- add the collections user which can only write data to the references table
CREATE ROLE collections NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN PASSWORD 'collections' VALID UNTIL 'infinity';
GRANT ALL ON collections_references TO collections;
GRANT SELECT, UPDATE ON "references" TO collections;
