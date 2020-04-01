import org.apache.commons.io.FileUtils;
import org.apache.http.HttpHost;
import org.apache.lucene.util.IOUtils;
import org.elasticsearch.action.bulk.BulkAction;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkRequestBuilder;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContentType;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class Fill {
    private static String host="localhost";
    private static int port=9200;
    private static RestHighLevelClient client;

    public static void main(String[] args) throws IOException {
        client = new RestHighLevelClient(
                RestClient.builder(
                        new HttpHost(host, port, "http")));

        BulkRequest request = new BulkRequest();
        String data = FileUtils.readFileToString(new File("data.json"), "UTF-8");
        System.out.println(data);
        for(int j=0;j<10;j++) {
            long time=System.currentTimeMillis();
            for (int i = 0; i < 1000; i++) {
                IndexRequest idx = new IndexRequest("search_idx").id(UUID.randomUUID().toString()).type("_doc")
                        .source(data, XContentType.JSON);
                request.add(idx);
                //client.index(idx, RequestOptions.DEFAULT);
            }
            System.out.println("Prepared " + (System.currentTimeMillis() - time) + "ms");
            client.bulk(request, RequestOptions.DEFAULT);
            System.out.println("Finished " + (System.currentTimeMillis() - time) + "ms ("+j+")");
        }
        client.close();
    }
}
