import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()


@mcp.tool()
async def searcher(
    search: str, max_results: int = 5, date_limited: bool = False
):
    """
    Searches arXiv for articles matching the search string.
    :param search: The string to search for.
    :param max_results: The maximum number of articles to return.
    :param date_limited: If True, only articles published today will be returned.
    """

    split_search = search.split(" ")

    def fill(find: dict, i: int, updated: str, published: str):
        find["update_date"] = updated
        find["published_date"] = published
        find["title"] = title_elems[i].find("title").text
        find["id"] = title_elems[i].find("id").text
        authors = title_elems[i].find_all("name")
        find["authors_len"] = len(authors)
        for j in range(len(authors)):
            find["author_" + str(j)] = authors[j].text
        find["abstract"] = title_elems[i].find("summary").text

    today = str(date.today() - timedelta(1))

    url = ["http://export.arxiv.org/api/query?search_query=all:"]
    for i in range(len(split_search)):
        if i != len(split_search) - 1:
            url.append(split_search[i] + "+AND+")
        else:
            url.append(split_search[i])
    url.append("&sortBy=lastUpdatedDate&sortOrder=descending&max_results=")
    url.append(str(max_results))
    url = "".join(url)

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "lxml")

    title_elems = soup.find_all("entry")
    finds = []
    for i in range(len(title_elems)):
        find = {}
        updated = title_elems[i].find("updated").text.split("T")[0]
        published = title_elems[i].find("published").text.split("T")[0]
        if date_limited is True:
            if today in set([updated, published]):
                fill(find, i, updated, published)
        else:
            fill(find, i, updated, published)
        if find:
            finds.append(find)


    print('arXivSearcher results for "' + search + '":\n')

    finds = list(reversed(finds))
    for i in range(len(finds)):
        print(
            "~" * 80
            + "\n"
            + "TITLE: "
            + str(finds[i]["title"])
            + "\n\n"
            + "URL: "
            + str(finds[i]["id"])
            + "\n\n"
            + "UPDATED: "
            + str(finds[i]["update_date"])
            + ", PUBLISHED: "
            + str(finds[i]["published_date"])
            + "\n\n"
            + "AUTHORS: "
            + ", ".join(
                [
                    finds[i]["author_" + str(j)]
                    for j in range(finds[i]["authors_len"])
                ]
            )
            + "\n\n"
            + "ABSTRACT: "
            + str(finds[i]["abstract"])
        )
    print(
        str(len(finds))
        + " results returned. Max search results set at "
        + str(max_results)
    )
    return finds


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
