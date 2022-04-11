import sys


class Category(object):
    SOCIALMEDIA = 1
    XXX         = 2
    BLOG        = 3
    ART         = 4
    PROGRAMMING = 5
    VIDEO       = 6
    MESSAGING   = 7
    DATING      = 8
    MUSIC       = 9
    SPORT       = 10
    MEMES       = 11
    OFFICE      = 12
    NEWS        = 13
    GAMES       = 14
    OTHER       = 15

    @classmethod
    def resolve(cls, category: str) -> int:
        try:
            return cls.__getattribute__(cls, category.upper())
        except AttributeError:
            print('That category doesn\'t exist!')
            sys.exit(0)

    @classmethod
    def to_list(cls) -> "list[str]":
        return [attr for attr in dir(cls) if attr.isupper()]


"""
url:         URL to which a GET request is send to. The URL must
             include the "{user}" placeholder, e.g. https://example.com/{user}
screen_url:  The URL that gets printed to the terminal. This might
             get used if the request url uses work arounds in
             order to get valid results. If this is not provided,
             the request url is printed. (OPTIONAL)
domain:      Domain of the url, e.g. example.com
err_pattern: A regex that matches the html code that gets returned when
             a username doesn't exist (404 Page). (OPTIONAL)
             Flags enabled: IGNORECASE, MULTI-LINE, MATCH-ALL
err_dot:     Boolean that indicates if the site responses with a false
             result if the username contains a dot, or if the
             website doesn't allow dots in usernames. (OPTIONAL)
err_url:     A regex that gets applied on the URL of the response.
             If it matches, the overall result is considered false.
             (OPTIONAL) Flags enabled: IGNORECASE
category:    A category that fits to the website.
"""
POOL = [
    {
        "url"          : "https://instagram.com/{user}/guides",
        "screen_url"   : "https://instagram.com/{user}",
        "domain"       : "instagram.com",
        "err_pattern"  : r"<title.*?>Page Not Found • Instagram</title>",
        "category"     : Category.SOCIALMEDIA,
    },
    {
        "url"          : "https://snapchat.com/add/{user}",
        "domain"       : "snapchat.com",
        "err_pattern"  : r"<span.*?>Sorry,.*?not\sfound</span>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://redbubble.com/people/{user}",
        "domain"       : "redbubble.com",
        "err_pattern"  : r"<h1>This is a lost cause\.</h1>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://reddit.com/user/{user}",
        "domain"       : "reddit.com",
        "err_pattern"  : r"<h3.*?>Sorry, nobody.*?name\.</h3>",
        "err_dot"      : True,
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://pinterest.com/{user}",
        "domain"       : "pinterest.com",
        "err_pattern"  : r"<title.*?>Pinterest.*?</title>",
        "category"     : Category.ART
    },
    {   # TODO
        "url"          : "",
        "domain"       : "twitter.com",
        "err_pattern"  : r"class=\"errorContainer\"",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://linktr.ee/{user}",
        "domain"       : "linktr.ee",
        "err_pattern"  : r"<title.*?>Linktree.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://tiktok.com/@{user}",
        "domain"       : "tiktok.com",
        "err_pattern"  : r"<title>Couldn't find this account.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://github.com/{user}",
        "domain"       : "github.com",
        "err_pattern"  : r"<title.*?>Page not found.*?</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://tellonym.me/{user}",
        "domain"       : "tellonym.me",
        "err_pattern"  : r"<div.*?Create an account.*?answer",
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://t.me/{user}",
        "domain"       : "telegram.com",
        "err_pattern"  : r"<i class=\"tgme_icon_user\"></i>",
        "err_url"      : r"telegram\.org",
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://deviantart.com/{user}",
        "domain"       : "deviantart.com",
        "err_pattern"  : r"<title.*?>DeviantArt: 404</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://instabio.cc/{user}",
        "domain"       : "instabio.cc",
        "err_pattern"  : r"<img.*?alt=\"404\">",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://youtube.com/c/{user}",
        "domain"       : "youtube.com",
        "err_pattern"  : r"<title.*?>404\sNot\sFound.*?</title>",
        "category"     : Category.VIDEO
    },
    {
        "url"          : "https://wattpad.com/user/{user}",
        "domain"       : "wattpad.com",
        "err_pattern"  : r"<title.*?>Wattpad -.*?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://tinder.com/@{user}",
        "domain"       : "tinder.com",
        "err_pattern"  : r"<title.*?>Tinder \| Dating, Make.*?</title>",
        "category"     : Category.DATING
    },
    {
        "url"          : "https://soundcloud.com/{user}",
        "domain"       : "soundcloud.com",
        "err_pattern"  : r"<title.*?>Something went wrong.*?</title>",
        "category"     : Category.MUSIC
    },
    {
        "url"          : "https://vk.com/{user}",
        "domain"       : "vk.com",
        "err_pattern"  : r"<title.*?>404 Not.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://ebay.com/usr/{user}",
        "domain"       : "ebay.com",
        "err_pattern"  : r"<title.*?>ebay profile - error.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://last.fm/user/{user}",
        "domain"       : "last.fm",
        "err_pattern"  : r"<title.*?>Page\sNot\sFound.*?</title>",
        "category"     : Category.MUSIC
    },
    {
        "url"          : "https://ask.fm/{user}",
        "domain"       : "ask.fm",
        "err_pattern"  : r"<title.*?>Ask\sand\sAnswer.*?</title>",
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://9gag.com/u/{user}",
        "domain"       : "9gag.com",
        "err_pattern"  : r"<title.*?Nothing\shere.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://quora.com/profile/{user}",
        "domain"       : "quora.com",
        "err_pattern"  : r"<title.*?error.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://flickr.com/photos/{user}",
        "domain"       : "flickr.com",
        "err_pattern"  : r"<h2 class=\"status.*?>404</h2>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://gitlab.com/{user}",
        "domain"       : "gitlab.com",
        "err_pattern"  : r"<title.*?>Sign in.*?</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://bigo.tv/en/{user}",
        "domain"       : "bigo.tv",
        "err_pattern"  : r"ignoreUids:\[\]",
        "category"     : Category.VIDEO
    },
    {
        "url"          : "https://pornhub.com/users/{user}",
        "domain"       : "pornhub.com",
        "err_pattern"  : r"<title.*?>Page Not Found</title>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://lnk.bio/{user}",
        "domain"       : "lnk.bio",
        "err_pattern"  : r"<title.*?>Not Found.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://campsite.bio/{user}",
        "domain"       : "campsite.bio",
        "err_pattern"  : r"<title.*?>Campsite</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://xhamster.com/users/{user}",
        "domain"       : "xhamster.com",
        "err_pattern"  : r"<title.*?>User not found</title>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://redtube.com/users/{user}",
        "domain"       : "redtube.com",
        "err_pattern"  : r"<title.*?>Page Not Found</title>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://odysee.com/@{user}",
        "domain"       : "odysee.com",
        "err_pattern"  : r"<title.*?>Odysee</title>",
        "category"     : Category.VIDEO
    },
    {
        "url"          : "https://xvideos.com/profiles/{user}",
        "domain"       : "xvideos.com",
        "err_pattern"  : r"<title.*?Unknown.*?XVIDEOS.*?</title>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://fandom.com/u/{user}",
        "domain"       : "fandom.com",
        "err_pattern"  : r"<title.*?Not Found</title>",
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://www.tripadvisor.com/Profile/{user}",
        "domain"       : "tripadvisor.com",
        "err_pattern"  : r"<title.*?404 Not Found.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://codewars.com/users/{user}",
        "domain"       : "codewars.com",
        "err_pattern"  : r"<title.*?Codewars \| Achieve.*?</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://wikipedia.org/wiki/User:{user}",
        "domain"       : "wikipedia.org",
        "err_pattern"  : r"<div.*?message.*?>\".*?\" is not registered on this wiki.*?</div>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://facebook.com/{user}",
        "domain"       : "facebook.com",
        "err_pattern"  : r"<head><meta",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://twitch.tv/{user}",
        "domain"       : "twitch.tv",
        "err_pattern"  : r"content='@twitch'><link",
        "category"     : Category.VIDEO
    },
    {
        "url"          : "https://spankbang.com/profile/{user}",
        "domain"       : "spankbang.com",
        "err_pattern"  : r"<title.*?Free Porn Videos.*?</title>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://quizlet.com/{user}",
        "domain"       : "quizlet.com",
        "err_pattern"  : r"<title.*?Page Unavailable.*?</title>",
        "err_url"      : r"\/\w+?\/\d{9}",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://chaturbate.com/{user}/",
        "domain"       : "chaturbate.com",
        "err_pattern"  : r"<h1>HTTP 404.*?</h1>",
        "err_url"      : r"(?:chaturbate\.com\/?)$",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://vimeo.com/{user}",
        "domain"       : "vimeo.com",
        "err_pattern"  : r"<title.*?VimeUhOh</title>",
        "category"     : Category.VIDEO
    },
    {
        "url"          : "https://valence.community/visualization/profile/{user}",
        "domain"       : "valence.community",
        "err_pattern"  : r"<title.*?valence</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://untappd.com/user/{user}",
        "domain"       : "untappd.com",
        "err_pattern"  : r"<title.*?Untappd \| 404</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.tumblr.com/",
        "domain"       : "tumblr.com",
        "err_pattern"  : r"<title.*?Not found\.</title>",
        "err_dot"      : True,
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://line.me/R/ti/p/@{user}",
        "domain"       : "line.me",
        "err_pattern"  : r"<p.*?404 Not Found</p>",
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://www.taringa.net/{user}",
        "domain"       : "taringa.net",
        "err_pattern"  : r"<title.*?>Taringa!.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://myspace.com/{user}",
        "domain"       : "myspace.com",
        "err_pattern"  : r"<h1>Page Not Found</h1>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://mix.com/{user}",
        "domain"       : "mix.com",
        "err_pattern"  : r"<title>Mix</title>",
        "err_dot"      : True,
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://{user}.skyrock.com/profil/",
        "domain"       : "skyrock.com",
        "err_pattern"  : r"<title.*?Page not Found.*?</title>",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://www.reverbnation.com/{user}",
        "domain"       : "reverbnation.com",
        "err_pattern"  : r"<title.*?Page not Found.*?</title>",
        "category"     : Category.MUSIC
    },
    {
        "url"          : "https://www.gaiaonline.com/profiles/{user}/",
        "domain"       : "gaiaonline.com",
        "err_pattern"  : r"<title.*?Error.*?</title>",
        "err_dot"      : True,
        "category"     : Category.GAMES
    },
    {
        "url"          : "https://weheartit.com/{user}",
        "domain"       : "weheartit.com",
        "err_pattern"  : r"<title.*?>The Page.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://spreely.com/{user}",
        "domain"       : "spreely.com",
        "err_pattern"  : r"<title.*?>Spreely.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://wt.social/u/{user}",
        "domain"       : "wt.social",
        "err_pattern"  : r"<title.*?404 Error.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://www.crunchyroll.com/user/{user}",
        "domain"       : "crunchyroll.com",
        "err_pattern"  : r"<title>Crunchyroll - Page not found</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://giphy.com/{user}",
        "domain"       : "giphy.com",
        "err_pattern"  : r"(?:<title.*?>404 Not Found</title>)|(?:<h1.*?Explore.*?</h1>)",
        "err_url"      : r".*?\/explore\/.*?",
        "category"     : Category.MEMES
    },
    {
        "url"          : "https://{user}.livejournal.com/",
        "domain"       : "livejournal.com",
        "err_pattern"  : r"<title.*?Unknown Journal</title>",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://www.prezi.community/u/{user}",
        "domain"       : "prezi.community",
        "err_pattern"  : r"<title.*?Prezi Community</title>",
        "category"     : Category.OFFICE
    },
    {
        "url"          : "https://www.strava.com/athletes/{user}",
        "domain"       : "strava.com",
        "err_pattern"  : r"<title.*?Strava \| Run and Cycling.*?</title>",
        "err_dot"      : True,
        "category"     : Category.SPORT
    },
    {
        "url"          : "https://www.chess.com/member/{user}",
        "domain"       : "chess.com",
        "err_pattern"  : r"<title.*?Missing Page</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://lichess.org/@/{user}",
        "domain"       : "lichess.org",
        "err_pattern"  : r"<title.*?Page Not Found.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.eporner.com/profile/{user}/",
        "domain"       : "eporner.com",
        "err_pattern"  : r"<strong.*?Profile not found\.</strong>",
        "category"     : Category.XXX
    },
    {
        "url"          : "https://bandcamp.com/{user}",
        "domain"       : "bandcamp.com",
        "err_pattern"  : r"<title.*?>Bandcamp</title>",
        "category"     : Category.MUSIC
    },
    {
        "url"          : "https://archive.org/details/@{user}",
        "domain"       : "archive.org",
        "err_pattern"  : r"<title.*?>cannot find.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.gutefrage.net/nutzer/{user}",
        "domain"       : "gutefrage.net",
        "err_pattern"  : r"<title.*?>Gutefrage.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://picsart.com/u/{user}",
        "domain"       : "picsart.com",
        "err_pattern"  : r"<title.*?>Page not found</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://disqus.com/by/{user}/?",
        "domain"       : "disqus.com",
        "err_pattern"  : r"<title.*?>Page not found.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.blogspot.com/",
        "domain"       : "blogspot.com",
        "err_pattern"  : r"https://www\.blogger\.com/create-blog\.g?defaultSubdomain=",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://{user}.webnode.com/",
        "domain"       : "webnode.com",
        "err_pattern"  : r"We are sorry, but the page .*?\.webnode\.com",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://sourceforge.net/u/{user}/profile/",
        "domain"       : "sourceforge.net",
        "err_pattern"  : r"<title.*?>Page not found.*?</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://news.ycombinator.com/user?id={user}",
        "domain"       : "ycombinator.com",
        "err_pattern"  : r"No such user\.",
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://about.me/{user}",
        "domain"       : "about.me",
        "err_pattern"  : r"<title.*?>about\.me</title",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://medium.com/@{user}",
        "domain"       : "medium.com",
        "err_pattern"  : r"<title.*?>Medium</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://www.goodreads.com/{user}",
        "domain"       : "goodreads.com",
        "err_pattern"  : r"<title.*?>Page not found</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://blip.fm/{user}",
        "domain"       : "blip.fm",
        "err_pattern"  : r"404.*?Page Not Found",
        "category"     : Category.MUSIC
    },
    {
        "url"          : "https://en.gravatar.com/{user}",
        "domain"       : "gravatar.com",
        "err_pattern"  : r"<title.*?>Gravatar.*?</title>",
        "err_url"      : r"profiles\/no-such-user",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.fiverr.com/{user}",
        "domain"       : "fiverr.com",
        "err_pattern"  : r"<title.*?>Fiverr -.*?</title>",
        "err_url"      : r"(?:fiverr\.com\/?)$",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://auth.geeksforgeeks.org/user/{user}/profile",
        "domain"       : "geeksforgeeks.org",
        "err_pattern"  : r"<title.*?>Login.*?</title>",
        "err_url"      : r".*?\?to=.*?",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://www.etsy.com/people/{user}",
        "domain"       : "etsy.com",
        "err_pattern"  : r"<title.*?>Etsy -.*?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://ifunny.co/user/{user}",
        "domain"       : "ifunny.co",
        "err_pattern"  : r"<title.*?>404 - page.*?</title>",
        "category"     : Category.MEMES
    },
    {
        "url"          : "https://www.memecenter.com/{user}",
        "domain"       : "memecenter.com",
        "err_pattern"  : r"<title.*?>Meme Center -.*?</title>",
        "category"     : Category.MEMES
    },
    {
        "url"          : "https://imgur.com/search?q=user:{user}",
        "screen_url"   : "https://imgur.com/user/{user}",
        "domain"       : "imgur.com",
        "err_pattern"  : r"Found.*?<i>0</i>.*?results for",
        "err_url"      : r"search\?q=.*?",
        "err_dot"      : True,
        "category"     : Category.MEMES
    },
    {
        "url"          : "https://shoptly.com/{user}",
        "domain"       : "shoptly.com",
        "err_pattern"  : r"<title.*?>Sell Digital.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://linkedin.com/in/{user}",
        "domain"       : "linkedin.com",
        "err_url"      : r"com\/authwall\?.*?",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.wordpress.com",
        "domain"       : "wordpress.com",
        "err_url"      : r"\/typo\/\?subdomain=.+?",
        "err_dot"      : True,
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://www.slideshare.net/{user}",
        "domain"       : "slideshare.net",
        "err_pattern"  : r"<title.*?>Username available</title>",
        "category"     : Category.OFFICE
    },
    {
        "url"          : "https://{user}.yelp.com/",
        "domain"       : "yelp.com",
        "err_url"      : r"yelp\.\w+?/(?:[^/?=]*?)$",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.weebly.com/",
        "domain"       : "weebly.com",
        "err_pattern"  : r"<title.*?>404 - Page.*?</title>",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://imageshack.com/user/{user}",
        "domain"       : "imageshack.com",
        "err_url"      : r"imageshack\.(?:\w+?\/?)$",
        "category"     : Category.SOCIALMEDIA
    },
    {   # TODO
        "url"          : "https://issuu.com/{user}",
        "domain"       : "issuu.com",
        "err_pattern"  : r"<title.*?>Issuu.*?</title>",
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://letterpile.com/@{user}",
        "domain"       : "letterpile.com",
        "err_pattern"  : r"<title.*?>LetterPile</title>",
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://hubpages.com/@{user}",
        "domain"       : "hubpages.com",
        "err_pattern"  : r"<title.*?>Page Not Found</title>",
        "err_dot"      : True,
        "category"     : Category.BLOG
    },
    {
        "url"          : "https://dzone.com/users/{user}",
        "domain"       : "dzone.com",
        "err_url"      : r"\/users\/(?:[^/?=]+?\/?)$",
        "err_dot"      : True,
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://www.pscp.tv/{user}",
        "domain"       : "pscp.tv",
        "err_pattern"  : r"<title.*?>404</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://dribbble.com/{user}/about",
        "domain"       : "dribbble.com",
        "err_pattern"  : r"<title.*?>Sorry, the page.*?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://dev.to/{user}",
        "domain"       : "dev.to",
        "err_pattern"  : r"<title.*?>The page you.*?</title>",
        "err_dot"      : True,
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://mastodon.social/@{user}",
        "domain"       : "mastodon.social",
        "err_pattern"  : r"<title.*?>The page you.*?</title>",
        "err_dot"      : True,
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://www.taskrabbit.com/profile/{user}",
        "domain"       : "taskrabbit.com",
        "err_url"      : r"taskrabbit\.(\w+?\/?)$",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://sharesome.com/api/users/{user}?stats=1&profile=1",
        "screen_url"   : "https://sharesome.com/{user}",
        "domain"       : "sharesome.com",
        "err_pattern"  : r"<title.*?>404 \|.*?</title>",
        "err_dot"      : True,
        "category"     : Category.XXX
    },
    {
        "url"          : "https://unsplash.com/@{user}",
        "domain"       : "unplash.com",
        "err_pattern"  : r"<title.*?>Page not found.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://steamcommunity.com/id/{user}",
        "domain"       : "steamcommunity.com",
        "err_pattern"  : r"<title.*?>.*?::\s*?Error.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.slack.com/",
        "domain"       : "slack.com",
        "err_pattern"  : r"<title.*?>There's been a gli.*?</title>",
        "err_dot"      : True,
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://meetme.com/{user}",
        "domain"       : "meetme.com",
        "err_url"      : r"meetme\.(?:\w+?\/?)$",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://ifttt.com/p/{user}",
        "domain"       : "ifttt.com",
        "err_pattern"  : r"<title.*?404 Error</title>",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://gitee.com/{user}",
        "domain"       : "gitee.com",
        "err_pattern"  : r"<title.*?\(404\)</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://coderwall.com/{user}",
        "domain"       : "coderwall.com",
        "err_pattern"  : r"<title.*?404 : Unable.*?</title>",
        "err_dot"      : True,
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://cash.app/${user}",
        "domain"       : "cash.app",
        "err_pattern"  : r"<title.*?Cash App - Page.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.buymeacoffee.com/{user}",
        "domain"       : "buymeacoffee.com",
        "err_pattern"  : r"<title.*?>Buy Me a Coffee -.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.canva.com/p/{user}/",
        "domain"       : "canva.com",
        "err_pattern"  : r"<title.*?>Amazingly Simple Graphic.*?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://www.buzzfeed.com/{user}",
        "domain"       : "buzzfeed.com",
        "err_pattern"  : r"<title.*?>Page not found</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://vsco.co/{user}/gallery",
        "domain"       : "vsco.co",
        "err_pattern"  : r"<title.*?>Page not found.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://curiouscat.live/api/v2.1/profile?username={user}",
        "screen_url"   : "https://curiouscat.live/{user}",
        "domain"       : "curiouscat.live",
        "err_pattern"  : r"\"profile_does_not_exist\"",
        "category"     : Category.MESSAGING
    },
    {
        "url"          : "https://independent.academia.edu/{user}",
        "domain"       : "academia.edu",
        "err_pattern"  : r"<title.*?>Academia\.edu</title>",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.producthunt.com/@{user}",
        "domain"       : "producthunt.com",
        "err_pattern"  : r"<title.*?>Product Hunt:.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://www.patreon.com/{user}/creators",
        "screen_url"   : "https://www.patreon.com/{user}",
        "domain"       : "patreon.com",
        "err_pattern"  : r"<span.*?>404</span>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://creativemarket.com/users/{user}",
        "domain"       : "creativemarket.com",
        "err_pattern"  : r"<title.*?>Whoomp, there.*?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://replit.com/@{user}",
        "domain"       : "replit.com",
        "err_pattern"  : r"<title.*?>Replit - 404 - Replit</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://itch.io/profile/{user}",
        "domain"       : "itch.io",
        "err_pattern"  : r"<title.*?>itch\.io</title>",
        "category"     : Category.GAMES
    },
    {
        "url"          : "https://www.pexels.com/@{user}",
        "domain"       : "pexels.com",
        "err_pattern"  : r"<title.*?>Error 404.*?</title>",
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://pastebin.com/u/{user}",
        "domain"       : "pastebin.com",
        "err_pattern"  : r"<title.*?>.+?Not Found.*?</title>",
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://{user}.jimdosite.com/",
        "domain"       : "jimdosite.com",
        "err_pattern"  : r"<head></head>",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://myanimelist.net/profile/{user}",
        "domain"       : "myanimelist.net",
        "err_pattern"  : r"<title.*?>404 Not.*?</title>",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://{user}.gumroad.com/",
        "domain"       : "gumroad.com",
        "err_pattern"  : r"<title.*?>Page not found.+?</title>",
        "err_dot"      : True,
        "category"     : Category.OTHER
    },
    {
        "url"          : "https://hackerone.com/{user}?type=user",
        "screen_url"   : "https://hackerone.com/{user}",
        "domain"       : "hackerone.com",
        "err_pattern"  : r"<h1>Page not found</h1>",
        "err_dot"      : True,
        "category"     : Category.PROGRAMMING
    },
    {
        "url"          : "https://flipboard.com/@{user}",
        "domain"       : "flipboard.com",
        "err_pattern"  : r"<title.*?>Flipboard:.+?</title>",
        "category"     : Category.NEWS
    },
    {
        "url"          : "https://ello.co/{user}",
        "domain"       : "ello.co",
        "err_pattern"  : r"<title.*?>.+?\[404\] Not Found</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://www.behance.net/{user}",
        "domain"       : "behance.net",
        "err_pattern"  : r"<title.*?>Behance ::.+?</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://www.plurk.com/{user}",
        "domain"       : "plurk.com",
        "err_pattern"  : r"<title.*?>User Not Found.*?</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://aminoapps.com/u/{user}",
        "domain"       : "aminoapps.com",
        "err_pattern"  : r"<title.*?>Amino</title>",
        "category"     : Category.ART
    },
    {
        "url"          : "https://meta.getaether.net/u/{user}",
        "domain"       : "getaether.net",
        "err_pattern"  : r"<title.*?>Meta Aether</title>",
        "category"     : Category.SOCIALMEDIA
    },
    {
        "url"          : "https://micro.blog/robertbrook",
        "domain"       : "micro.blog",
        "err_pattern"  : r"<body>User not found</body>",
        "category"     : Category.BLOG
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    },
    {
        "url"          : "",
        "domain"       : "",
        "err_pattern"  : r"",
        "category"     : Category
    }
]
