import wikipedia
import pageviewapi.period
from logger import get_logger

log = get_logger(__name__)

def tokenize(s):
    return s.lower() #replace("\n", "").replace(" ", "")

def get_best_option(options):
    max_opt = ("", 0)
    for opt in options:
        #print("trying opt:", opt)
        try:
            cur_count = pageviewapi.period.sum_last('en.wikipedia', opt, last=100)
        except pageviewapi.client.ZeroOrDataNotLoadedException as e:
            cur_count = 0
        #print("count:", cur_count)
        if (cur_count > max_opt[1]):
            max_opt = (opt, cur_count)
    log.info("choosed" + max_opt[0] + "as the default")
    page = wikipedia.page(max_opt[0])
    return page

def search_entity(name, fact):
    try:    
        page = wikipedia.page(wikipedia.search(name)[0])
        #print(page.title)
    except wikipedia.exceptions.DisambiguationError as e:
        log.info("To many options for the search phase")
        page = get_best_option(e.options)
    # found correct page
    return tokenize(fact) in tokenize(page.content)


def test():
    log.info("Did george clooney won academy awards?" + str(search_entity("George Clooney", "Academy Awards")))
    log.info("is barack obama black?" + str(search_entity("Barack Obama", "black")))
    log.info("bush is a woman?" + str(search_entity("bush", "woman")))


if __name__ == "__main__":
    test()
