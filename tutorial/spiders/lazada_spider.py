from __future__ import unicode_literals
import scrapy
import json
import io
import shutil
import jsonpath


class LazadaSpider(scrapy.Spider):
    name = "lazada"
    count = 0
    headers={
            ":authority": "www.lazada.vn",
            ":method": "GET",
            ":path": "/catalog/?q=bluetooth&_keyori=ss&from=input&spm=a2o4n.home.search.go.1905e182wu0KEQ",
            ":scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "cookie": "_uab_collina=155307636820552928327088; t_fv=1553076349079; t_uid=HyivQOxuSxfWbio8IELJLZN3NVVAI5pz; t_sid=x9UPH2sa0M60NszriS24tGaqNErEvrNG; utm_channel=NA; lzd_cid=94668b75-72cd-4530-9dd0-cee038cef1d1; cna=b352FGfLdGICAXFDnWUCWPEf; hng=VN|en|VND|704; userLanguageML=en; lzd_sid=15e4cd4f3de82ad5589adfca515d6fb2; _m_h5_tk=a65de5683faee9802330a3c4a82cb61e_1553083910241; _m_h5_tk_enc=89e17c490b2a83f0e01b18def2ef2693; _bl_uid=14j6gtzRhvk1g7kem5zCggwq9gky; cto_lwid=b932e3e6-7688-4a64-ba1a-bf35545a8f18; _fbp=fb.1.1553076351000.1078085453; _tb_token_=e961037667fee; JSESSIONID=F77EB00E9EC3285547D73346D9488D05; isg=BDEx6aSYyVKtgWVGk4sKvsbBQLQLtqQrbCOP2xNGTvgXOlCMW2ojYJtTWIb58j3I; l=bBOn42oqvp-nc49xBOCwNuI8LDQ9hIRfguPRwCqJi_5Bv1T_IW6Olt5YTe96Vf5l_Z8B4J-HftpTfUI4PQC..",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36"
    }

    def start_requests(self):
        '''urls = [ 'https://www.lazada.vn/catalog/?q=bluetooth&_keyori=ss&from=input&spm=a2o4n.home.search.go.1905e182wu0KEQ'
        ]'''
        urls=[51]
        for i in range(1,52):
            urls.append('https://www.lazada.vn/catalog/?q=bluetooth&_keyori=ss&from=input&spm=a2o4n.home.search.go.1905e182wu0KEQ&page=%s' % str(i))
        for i in range(1,52):
            print "Request url %s" % urls[i]
            yield scrapy.Request(url=urls[i], callback=self.parse, headers=self.headers)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'lazada/listItems-%s.json' % self.count
        self.count += 1
        script = response.css('script::text')[1].get()[16:]
        pretty =json.dumps(json.loads(script),ensure_ascii=False,indent=4,sort_keys=True)
        data =jsonpath.jsonpath(json.loads(pretty),'$..listItems')
        pretty =json.dumps(data,ensure_ascii=False,indent=4,sort_keys=True)
        '''print "Json Path Data %s" % data'''

        '''print pretty'''
        with io.open(filename, mode='w+',encoding='utf8') as f:
            f.write(pretty)
        self.log('Saved file %s' % filename)
