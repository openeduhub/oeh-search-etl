###### Description
In this directory you can find the various "mds_oeh.xml" (Metadatasets for Open Edu Hub) files provided by Edu-Sharing/Metaventis company. In this file we attempt to provide am overview of the changes across the different provided versions of the file.

The "curl_metadatasetsV2.sh" file is part of the Docker execution to let the system know about the included metadatasets file.

###### Versions of mds_oeh.xml

- mds_oeh_24_06_2020.xml: The first provided file. 
- mds_oeh_11_09_2020.xml: Introduced the "ngsearch" query, originally only provided by the default metadatasets file, mds.xml. Changes in content element fields, default collections sorting by creation date. 
- mds_oeh_17_09_2020.xml: Added the "ccm:replicationsourceuuid" property field in the Collections query, s.t. it can be queried and changed its format in the "DSL" query format. It should be now available for Solr and probably for Elasticsearch as well.

