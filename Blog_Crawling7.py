# total_page 전체 출력하는 코드에 함수 연결

import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

keyword = "테슬라"

blog_urls = []        
Blog = []

def get_blog(blog_url):
    
    h = {
        "Cookie":"NNB=EBHCWBDFIDSGI; nx_ssl=2; page_uid=ieSqHsprvh8ssOq4u60ssssssjZ-408641; _naver_usersession_=mZFsErGp5iGCcsxY3NW26A=="
        , "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    res = requests.get(blog_url, headers=h)
    soup = BeautifulSoup(res.text, "html.parser")

    print(blog_url)

    if "naver" in blog_url:
        # 네이버 블로그
        if soup.select_one(".pcol1 span") != None:
            category = soup.select_one(".blog2_series a").text
            title = soup.select_one(".pcol1 span").text
            writer = soup.select_one(".nick a").text
            date = soup.select_one(".se_publishDate.pcol2").text
            content = soup.select_one(".se-main-container").text.replace("\n", "").strip()

        elif soup.select_one(".se_textarea") != None:
            category = soup.select_one(".blog2_series a").text
            title = soup.select_one(".se_textarea").text.replace("\n", "").strip()
            writer = soup.select_one(".nick a").text
            date = soup.select_one(".se_publishDate.pcol2").text
            content = soup.select_one(".se_component_wrap.sect_dsc.__se_component_area").text.replace("\n", "").strip()

        elif soup.select_one("h3.se_textarea") != None:
            category = soup.select_one(".blog2_series a").text
            title = soup.select_one("h3.se_textarea").text
            writer = soup.select_one(".nick a").text
            date = soup.select_one(".se_publishDate.pcol2").text
            content = soup.select_one(".se_textarea").text.replace("\n", "").strip()

        elif soup.select_one("span#blogTitleName") != None:
            category = soup.select_one("span.cate.pcol2 a.pcol2").text
            title = soup.select_one("span.pcol1.itemSubjectBoldfont").text
            writer = soup.select_one("span#blogTitleName").text
            date = soup.select_one("p.date.fil5.pcol2._postAddDate").text
            content = soup.select_one("div#postViewArea").text.replace("\n", "").strip()

        # elif soup.select_one("strong.user_blog_name") != None:
        #     category = soup.select_one("span.cate.pcol2").text.split("/")[0].strip() + " /" + soup.select_one("span.cate.pcol2").text.split("/")[1]
        #     title = soup.select_one("span.pcol1.itemSubjectBoldfont").text
        #     writer = soup.select_one("strong.user_blog_name").text
        #     date = soup.select_one("p.date.fil5.pcol2._postAddDate").text
        #     content = soup.select_one("div#postViewArea").text.replace("\n", "").strip()

        elif soup.select_one("a.pcol2") != None:
            category = soup.select_one("span.cate.pcol2 a.pcol2").text
            title = soup.select_one("span.pcol1.itemSubjectBoldfont").text
            # writer가 없는데?
            writer = "오토헤럴드"
            date = soup.select_one("p.date.fil5.pcol2._postAddDate").text
            content = soup.select_one("div#postViewArea").text.replace("\n", "").strip()
        
        else:
            print("다른 타입의 네이버 블로그: ", blog_url)
            
    else:

        if soup.select_one("h2.screen_out") != None:
            category = "접근이 제한된 블로그입니다."
            title = "접근이 제한된 블로그입니다."
            writer = "접근이 제한된 블로그입니다."
            date = "접근이 제한된 블로그입니다."
            content = "접근이 제한된 블로그입니다."

        # yes24 블로그
        elif soup.select_one("#cphMain_dlArtList_lbArtCateNm_0") != None:
            category = soup.select_one("#cphMain_dlArtList_lbArtCateNm_0").text
            title = soup.select_one("#cphMain_dlArtList_lbArtTitle_0").text
            writer = soup.select_one("#ImgLayer").text
            date = soup.select_one("#cphMain_dlArtList_lbWriteDate_0").text
            content = soup.select_one("#cphMain_dlArtList_lbArtCont_0").text.replace("\n", "").strip()

        elif soup.select_one("p.txt_sub_tit") != None:
            category = soup.select_one("span.category").text.strip()
            title = soup.select_one("p.txt_sub_tit").text
            writer = soup.select_one("span.name").text.split(" ")[1]
            date = soup.select_one("span.date").text
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        # 티스토리 블로그
        elif soup.select_one(".hgroup .category") != None:
            category = soup.select_one(".hgroup .category").text
            title = soup.select_one(".hgroup h1").text
            writer = soup.select_one(".author").text
            date = soup.select_one(".date").text
            content = soup.select_one(".entry-content p").text
        
        elif soup.select_one(".box-meta p") != None:
            category = soup.select_one(".box-meta p").text
            title = soup.select_one(".box-meta h2").text
            writer = soup.select_one(".writer").text
            date = soup.select_one(".date")
            content = soup.select_one(".article-view").text.replace("\n", "").strip()

        elif soup.select_one(".post-cover .inner h1") != None:
            category = soup.select_one(".inner .category").text
            title = soup.select_one(".post-cover .inner h1").text
            writer = soup.select_one(".author").text[3:]
            date = soup.select_one(".date").text
            content = soup.select_one(".entry-content").text.replace("\n", "").strip()
            
        elif soup.select_one(".info_post") != None:
            category = soup.select_one(".tit_category").text
            title = soup.select_one("h3.tit_post").text
            writer = soup.select_one(".info_post").text.split("\n")[0]
            date = soup.select_one(".info_post").text.split("\n")[1].strip()
            content = soup.select_one(".contents_style p").text

        elif soup.select_one("span.txt_detail") != None:
            category = soup.select_one(".tit_category").text
            title = soup.select_one("h3.tit_post").text
            writer = soup.select_one("span.txt_detail").text.split("\n")[0]
            date = soup.select_one("span.txt_detail").text.split("\n")[1].strip()
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("strong.title_view") != None:
            category = soup.select_one("span.category").text
            title = soup.select_one("strong.title_view").text
            writer = soup.select_one("span.title_text").text
            date = soup.select_one("span.date").text
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one(".titleWrap.jumbotron span a") != None:
            category = soup.select_one(".titleWrap.jumbotron span a").text
            title = soup.select_one(".titleWrap.jumbotron a").text
            writer = soup.select_one(".navbar-header a")["title"]
            date = soup.select_one(".date.label.label-info").text
            content = soup.select_one(".tt_article_useless_p_margin.contents_style p").text

        elif soup.select_one(".jb-article-information-category span a") != None:
            category = soup.select_one(".jb-article-information-category span a").text
            title = soup.select_one(".jb-content-title.jb-content-title-article h2 a").text
            writer = soup.select_one(".jb-site-title a span").text
            date = soup.select_one(".jb-article-information-date span").text.replace("\n", "").strip()
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one(".txt_detail.my_post") != None:
            category = soup.select_one(".tit_category a").text
            title = soup.select_one(".tit_post a").text
            writer = soup.select_one(".txt_detail.my_post").text.split("\n")[0]
            date = soup.select_one(".txt_detail.my_post").text.split("\n")[1].strip()
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("td.branch3 #text_588083") != None:
            category = soup.select_one("td.branch3 #text_588083").text
            title = soup.select_one(".titleWrap h2 a").text
            writer = soup.select_one(".module.module_plugin center p b a").text[:5]
            date = title[4:16]
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one(".categories a") != None:
            category = soup.select_one(".categories a").text
            title = soup.select_one(".post h2 a").text
            writer = soup.select_one("#bloginfo b").text
            date = soup.select_one(".date").text
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one(".content-title .inner .category") != None:
            category = soup.select_one(".content-title .inner .category").text
            title = soup.select_one(".title-box h1").text
            writer = soup.select_one(".author").text
            date = soup.select_one(".date").text
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("strong.title_post") != None: 
            category = soup.select_one("p.info").text.split("ㆍ")[1]
            title = soup.select_one("strong.title_post").text
            writer = soup.select_one("a.link_logo").text.replace("\n", "").strip()
            date = soup.select_one("p.info").text.split("ㆍ")[0]
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("a.category") != None:
            category = soup.select_one("a.category").text
            title = soup.select_one("div.heading h1.title").text
            writer = soup.select_one("div.user").text
            date = soup.select_one("time.date").text
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("h1.hd-heading.lts-narrow.p-name a") != None:
            category = soup.select_one("a.p-category.target-bread").text
            title = soup.select_one("h1.hd-heading.lts-narrow.p-name a").text
            writer = soup.select_one("span.p-author.h-card").text
            date = soup.select_one("abbr.timeago.dt-published").text
            content = soup.select_one("div.tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()    

        elif soup.select_one("div#head") != None:
            category = soup.select_one("div#head h2 a").text.split("]")[0][1:]
            title = soup.select_one("div#head h2 a").text
            writer = soup.select_one("div#sidebar h1 a").text
            date = soup.select_one("div.date").text
            content = soup.select_one("div.contents_style").text.replace("\n", "").strip()

        # 알라딘 블로그
        elif soup.select_one(".titlebox h2") != None:
            title = soup.select_one(".titlebox h2").text.strip().split("ｌ")[0]
            category = soup.select_one(".titlebox h2").text.strip().split("ｌ")[1]
            writer = soup.select_one(".fr h4 a").text
            date = soup.select_one(".fr h4").text.split("\n")[-2].strip()
            content = soup.select_one(".article p").text.replace("\n", "").strip()

        # 기타 블로그            
        elif soup.select_one(".site-description") != None:
            category = soup.select_one(".site-description").text
            title = soup.select_one(".entry-title").text
            writer = soup.select_one(".author.vcard a").text
            date = soup.select_one(".entry-date.published").text
            content = soup.select_one(".contents_style").text.replace("\n", "").strip()

        elif soup.select_one("#menu-item-22049 a") != None:
            category = soup.select_one("#menu-item-22049 a").text
            title = soup.select_one(".entry-title").text
            writer = soup.select_one(".copyright-bar").text.split("-")[1].split("@")[0].strip()
            date = soup.select_one(".entry-date.published").text
            content = soup.select_one(".entry-content").text.replace("\n", "").strip()

        elif soup.select_one(".titleWrap h2 a") != None:
            category = soup.select_one(".category a").text
            title = soup.select_one(".titleWrap h2 a").text
            writer = soup.select_one(".text").text.split(" ")[-1]
            date = soup.select_one(".date").text
            content = soup.select_one(".contents_style").text.replace("\n", "").strip()

        elif soup.select_one(".hgroup .category") != None:
            category = soup.select_one(".hgroup .category").text
            title = soup.select_one(".hgroup h1").text
            writer = soup.select_one(".author").text
            date = soup.select_one(".date").text.replace("\n", "").strip()
            content = soup.select_one(".tt_article_useless_p_margin.contents_style").text.replace("\n", "").strip()

        elif soup.select_one("h1.entry-title") != None:
            category = "카테고리 없음"
            title = soup.select_one("h1.entry-title").text
            writer = soup.select_one("span.author-name").text
            date = soup.select_one("time.entry-date.published").text
            content = soup.select_one("div.entry-content").text.replace("\n", "").strip()

        # MileMoa 블로그
        elif soup.select_one("div.document_9529583_3896185.xe_content") != None:
            category = soup.select_one("ol.lb-bc").text.split("\n")[-4].strip()
            title = soup.select_one("a.lb-dm-link.lb-link").text.replace("\n", "").strip()
            writer = soup.select_one("p.lb-dm-info").text.replace("\n", "").strip().split(",")[0]
            date = soup.select_one("p.lb-dm-info").text.replace("\n", "").strip().split(",")[1].strip()
            content = soup.select_one("div.document_9529583_3896185.xe_content").text.replace("\n", "").strip()

        elif soup.select_one("div.document_9527862_3431968.xe_content") != None:
            category = soup.select_one("ol.lb-bc").text.split("\n")[-4].strip()
            title = soup.select_one("a.lb-dm-link.lb-link").text.replace("\n", "").strip()
            writer = soup.select_one("p.lb-dm-info").text.replace("\n", "").strip().split(",")[0]
            date = soup.select_one("p.lb-dm-info").text.replace("\n", "").strip().split(",")[1].strip()
            content = soup.select_one("div.document_9527862_3431968.xe_content").text.replace("\n", "").strip()
        
        elif soup.select_one("div.document_9527862_3431968.xe_content") != None:
            category = soup.select_one("div#lb_bc").text.split("\n")[11].strip()
            title = soup.select_one("a.lb-dm-link.lb-link").text.strip()
            writer = soup.select_one("p.lb-dm-info").text.split(",")[0].strip()
            date = soup.select_one("p.lb-dm-info").text.split(",")[1].strip()
            content = soup.select_one("div.document_9527862_3431968.xe_content").text.replace("\n", "").strip()

        elif soup.select_one("div.document_9531101_978571.xe_content") != None:
            category = soup.select_one("div#lb_bc").text.split("\n")[-4].strip()
            title = soup.select_one("a.lb-dm-link.lb-link").text
            writer = soup.select_one("p.lb-dm-info").text.split(",")[0].strip()
            date = soup.select_one("p.lb-dm-info").text.split(",")[1].strip()
            content = soup.select_one("div.document_9531101_978571.xe_content").text.replace("\n", "").strip()

        else:
            print("다른 타입의 블로그: ", blog_url)
            
    Blog.append((category, title, writer, date, content, blog_url))

    return Blog

    # except:
    #     if soup.select_one("strong.tit_error.tit_error_type2") != None:
    #         return print("접근이 제한된 블로그입니다.")


def get_blog_list(keyword, start_date, end_date):

    page = 1
    while True:
        h = {
            "Cookie":"NNB=EBHCWBDFIDSGI; nx_ssl=2; page_uid=ieSqHsprvh8ssOq4u60ssssssjZ-408641; _naver_usersession_=mZFsErGp5iGCcsxY3NW26A=="
            , "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        print("page: ", page)
        start = (page - 1) * 30 + 1

        URL = f"https://s.search.naver.com/p/blog/search.naver?where=blog&sm=tab_pge&api_type=1&query={keyword}&rev=44&start={start}&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Add%2Cp%3Afrom{end_date}to{start_date}&nlu_query=%7B%22r_category%22%3A%2233+25%22%7D&dkey=0&source_query=&nx_search_query={keyword}&spq=0&_callback=viewMoreContents"
        res = requests.get(URL, headers=h)

        try:
            for data in re.finditer("\{.*\}", res.text):
                data = json.loads(data.group())
                total_page = int(data["total"]) // 30
                soup = BeautifulSoup(data["html"], "html.parser")    
        except:
            for data in re.finditer("\{.*\}", res.text):        
                total_page = int(data.group().split(",")[0].split(":")[1].replace('"', "")) // 30 
                for data in re.finditer("\<[^\>]*\>.*", data.group()):
                    soup = BeautifulSoup(data.group().replace("}", ""), "html.parser")

        blogs = []
        for a in soup.select(".total_area a"):
            if a["class"] == ['api_txt_lines', 'total_tit']:
                blogs.append(a["href"])

        for blog in blogs:
            if not("naver" in blog):
                blog_url = blog
            else:
                blogId = blog.split("/")[-2]
                logNo = blog.split("/")[-1]

                blog_url = f"https://blog.naver.com/PostView.naver?blogId={blogId}&logNo={logNo}" 

            blog_urls.append(get_blog(blog_url))

        if page == total_page:
            break

        page += 1

    return pd.DataFrame(Blog, columns = ["카테고리", "제목", "작성자", "작성일시", "원문", "URL"])

print(get_blog_list("테슬라", "20220921", "20220922"))
    
    
        
    

    


