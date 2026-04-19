"""Web scraper for La Nación crime news using Scrapling."""

import json
import re
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field
from scrapling import Fetcher
from scrapling.fetchers import DynamicSession


class ScrapedArticle(BaseModel):
    """Data model for a scraped news article."""

    title: str = Field(..., description="Article headline")
    url: str = Field(..., description="Full URL to the article")
    description: str = Field(..., description="Article summary/description")
    publication_date: datetime = Field(..., description="Publication timestamp")
    article_id: str = Field(..., description="Unique article identifier")
    image_url: str | None = Field(None, description="Featured image URL")
    full_content: str | None = Field(None, description="Full article text content")


class LaNacionCrimeScraper:
    """Scraper for La Nación crime news section."""

    BASE_URL = "https://www.nacion.com"
    CRIME_SECTION_URL = f"{BASE_URL}/sucesos/crimenes/"

    def __init__(self) -> None:
        """Initialize the scraper with Scrapling Fetcher."""
        self.fetcher = Fetcher(auto_match=True)

    def scrape_articles_with_pagination(
        self, max_articles: int = 50, fetch_full_content: bool = True
    ) -> list[ScrapedArticle]:
        """Scrape crime news articles using DynamicFetcher for pagination.

        This method uses Scrapling's DynamicFetcher to handle the 'Ver más' button
        that loads more articles progressively.

        Args:
            max_articles: Maximum number of articles to return (default: 50)
            fetch_full_content: Whether to fetch full article content (default: True)

        Returns:
            List of scraped articles

        Raises:
            RuntimeError: If scraping fails
        """
        try:
            with DynamicSession(headless=True, disable_resources=False) as session:
                # Get the Playwright page object from session
                # Note: We need to get the page BEFORE fetching, or navigate it directly
                pages = session.context.pages
                if not pages:
                    # Create a new page if none exists
                    page = session.context.new_page()
                else:
                    page = pages[0]

                # Navigate to the page directly using Playwright
                page.goto(self.CRIME_SECTION_URL, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)  # Wait for initial content

                # Click "Ver más" button repeatedly until we have enough articles
                previous_count = 0
                max_clicks = 20  # Safety limit (each click loads ~5 articles)
                clicks = 0
                no_change_count = 0  # Track how many times count didn't change

                while clicks < max_clicks:
                    # Count current articles
                    current_count = page.evaluate("""
                        () => {
                            const containers = document.querySelectorAll('article, .results-list--description-author-container');
                            const urls = new Set();
                            containers.forEach(container => {
                                const links = container.querySelectorAll('a[href*="/sucesos/"]');
                                links.forEach(link => {
                                    const href = link.getAttribute('href');
                                    if (href && href.includes('/story/')) {
                                        urls.add(href);
                                    }
                                });
                            });
                            return urls.size;
                        }
                    """)

                    # Stop if we have enough articles
                    if current_count >= max_articles:
                        break

                    # Stop if count hasn't changed for 2 consecutive clicks
                    if current_count == previous_count:
                        no_change_count += 1
                        if no_change_count >= 2:
                            break  # No new articles loaded twice in a row
                    else:
                        no_change_count = 0  # Reset counter

                    previous_count = current_count

                    # Try to find and click "Ver más" button
                    button_clicked = page.evaluate("""
                        () => {
                            const button = Array.from(document.querySelectorAll('button'))
                                .find(btn => btn.textContent.trim() === 'Ver más');
                            if (button) {
                                button.click();
                                return true;
                            }
                            return false;
                        }
                    """)

                    if not button_clicked:
                        break  # No more "Ver más" button

                    clicks += 1
                    page.wait_for_timeout(3000)  # Wait for new content to load

                # Extract all article data using Playwright
                articles_data = page.evaluate("""
                    () => {
                        const articles = [];
                        const seen = new Set();

                        // Helper to parse an element
                        const parseElement = (element, selector) => {
                            const link = element.querySelector(selector);
                            if (!link) return null;

                            const url = link.getAttribute('href');
                            if (!url || !url.includes('/sucesos/')) return null;
                            if (seen.has(url)) return null;
                            seen.add(url);

                            const title = link.textContent.trim();
                            const timeElem = element.querySelector('time');
                            const datetime = timeElem ? timeElem.getAttribute('datetime') : null;
                            const descElem = element.querySelector('p.description-text, p');
                            const description = descElem ? descElem.textContent.trim() : title;

                            // Try multiple selectors for images
                            let imageUrl = null;
                            const imgElem = element.querySelector('img.c-image, img[src*="resizer"], img[loading="lazy"], img');
                            if (imgElem) {
                                imageUrl = imgElem.getAttribute('src') || imgElem.getAttribute('data-src');
                            }

                            return { url, title, datetime, description, imageUrl };
                        };

                        // Parse <article> elements
                        document.querySelectorAll('article').forEach(article => {
                            const data = parseElement(article, 'h3.c-heading a, a');
                            if (data) articles.push(data);
                        });

                        // Parse results-list containers
                        document.querySelectorAll('.results-list--description-author-container').forEach(container => {
                            const link = container.querySelector('a');
                            if (!link) return;

                            const url = link.getAttribute('href');
                            if (!url || !url.includes('/sucesos/')) return;
                            if (seen.has(url)) return;
                            seen.add(url);

                            const title = link.textContent.trim();
                            const timeElem = container.querySelector('time');
                            const datetime = timeElem ? timeElem.getAttribute('datetime') : null;
                            const descElem = container.querySelector('p.description-text, p');
                            const description = descElem ? descElem.textContent.trim() : title;

                            // For results-list, image is in parent element
                            let imageUrl = null;
                            const parent = container.parentElement;
                            if (parent) {
                                const imgElem = parent.querySelector('img');
                                if (imgElem) {
                                    imageUrl = imgElem.getAttribute('src') || imgElem.getAttribute('data-src');
                                }
                            }

                            articles.push({ url, title, datetime, description, imageUrl });
                        });

                        return articles;
                    }
                """)

                # Convert to ScrapedArticle objects
                unique_articles = []
                for data in articles_data:
                    url = data["url"]
                    if url.startswith("/"):
                        url = f"{self.BASE_URL}{url}"

                    # Parse datetime
                    pub_date = datetime.now(UTC)
                    if data.get("datetime"):
                        try:
                            pub_date = datetime.fromisoformat(
                                data["datetime"].replace("Z", "+00:00")
                            )
                        except (ValueError, AttributeError):
                            pass

                    # Extract article ID
                    article_id = (
                        url.split("/")[-2] if "/story/" in url else url.split("/")[-1]
                    )

                    article = ScrapedArticle(
                        title=data["title"],
                        url=url,
                        description=data.get("description") or data["title"],
                        publication_date=pub_date,
                        article_id=article_id,
                        image_url=data.get("imageUrl"),
                    )
                    unique_articles.append(article)

                # Limit to max_articles
                unique_articles = unique_articles[:max_articles]

                # Fetch full content if requested
                if fetch_full_content:
                    for article in unique_articles:
                        try:
                            article.full_content = self.scrape_article_content(
                                article.url
                            )
                        except RuntimeError:
                            article.full_content = None

                return unique_articles

        except Exception as e:
            raise RuntimeError(f"Failed to scrape articles with pagination: {e}") from e

    def _parse_article_from_element(self, article_elem) -> ScrapedArticle | None:
        """Parse article from <article> element."""
        try:
            title_link = article_elem.css("h3.c-heading a").first
            if not title_link:
                return None

            title = title_link.text.strip()
            url = title_link.attrib.get("href", "")

            if url.startswith("/"):
                url = f"{self.BASE_URL}{url}"

            if "/sucesos/" not in url:
                return None

            desc_elem = article_elem.css("p.description-text").first
            description = desc_elem.text.strip() if desc_elem else title

            pub_date = datetime.now(UTC)
            time_elem = article_elem.css("time").first
            if time_elem and time_elem.attrib.get("datetime"):
                datetime_str = time_elem.attrib.get("datetime", "")
                if datetime_str:
                    try:
                        pub_date = datetime.fromisoformat(
                            datetime_str.replace("Z", "+00:00")
                        )
                    except ValueError:
                        pass

            article_id = url.split("/")[-2] if "/story/" in url else url.split("/")[-1]
            img_elem = article_elem.css("img.c-image").first
            image_url = img_elem.attrib.get("src") if img_elem else None

            return ScrapedArticle(
                title=title,
                url=url,
                description=description,
                publication_date=pub_date,
                article_id=article_id,
                image_url=image_url,
            )
        except (AttributeError, IndexError, KeyError):
            return None

    def _parse_article_from_results_container(self, container) -> ScrapedArticle | None:
        """Parse article from .results-list--description-author-container element."""
        try:
            link = container.css("a").first
            if not link:
                return None

            title = link.text.strip()
            url = link.attrib.get("href", "")

            if url.startswith("/"):
                url = f"{self.BASE_URL}{url}"

            if "/sucesos/" not in url:
                return None

            desc_elem = container.css("p.description-text, p").first
            description = desc_elem.text.strip() if desc_elem else title

            pub_date = datetime.now(UTC)
            time_elem = container.css("time").first
            if time_elem and time_elem.attrib.get("datetime"):
                datetime_str = time_elem.attrib.get("datetime", "")
                if datetime_str:
                    try:
                        pub_date = datetime.fromisoformat(
                            datetime_str.replace("Z", "+00:00")
                        )
                    except ValueError:
                        pass

            article_id = url.split("/")[-2] if "/story/" in url else url.split("/")[-1]

            return ScrapedArticle(
                title=title,
                url=url,
                description=description,
                publication_date=pub_date,
                article_id=article_id,
                image_url=None,
            )
        except (AttributeError, IndexError, KeyError):
            return None

    def _extract_json_data(self, html_content: str) -> dict[str, Any]:
        """Extract JSON data embedded in the page.

        Args:
            html_content: Raw HTML content from the page

        Returns:
            Parsed JSON data containing article information

        Raises:
            ValueError: If JSON data cannot be found or parsed
        """
        # Look for Fusion data structure in script tags
        pattern = r"<script[^>]*>\s*Fusion\.globalContent\s*=\s*({.*?});\s*</script>"
        match = re.search(pattern, html_content, re.DOTALL)

        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse Fusion.globalContent JSON: {e}"
                ) from e

        # Alternative: Look for story-feed-sections data
        pattern = r'"story-feed-sections"[^{]*({[^}]*})'
        match = re.search(pattern, html_content)

        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse story-feed-sections JSON: {e}"
                ) from e

        raise ValueError("Could not find JSON data in page content")

    def _parse_article(self, article_data: dict[str, Any]) -> ScrapedArticle | None:
        """Parse a single article from JSON data.

        Args:
            article_data: Raw article data dictionary

        Returns:
            ScrapedArticle object or None if parsing fails
        """
        try:
            # Extract basic information
            article_id = article_data.get("_id", "")
            title = article_data.get("headlines", {}).get("basic", "")
            description = article_data.get("description", {}).get("basic", "")

            # Get URL
            url_path = (
                article_data.get("websites", {})
                .get("la-nacion", {})
                .get("website_url", "")
            )
            full_url = f"{self.BASE_URL}{url_path}" if url_path else ""

            # Parse publication date
            date_str = article_data.get("display_date", "")
            if date_str:
                pub_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            else:
                pub_date = datetime.now(UTC)

            # Get image URL
            image_url = None
            promo_items = article_data.get("promo_items", {})
            if isinstance(promo_items, dict):
                basic_promo = promo_items.get("basic", {})
                if isinstance(basic_promo, dict):
                    image_url = basic_promo.get("url")

            # Validate required fields
            if not title or not full_url:
                return None

            return ScrapedArticle(
                title=title,
                url=full_url,
                description=description or title,
                publication_date=pub_date,
                article_id=article_id,
                image_url=image_url,
            )

        except (KeyError, ValueError, TypeError):
            return None

    def scrape_articles(
        self, max_articles: int = 20, fetch_full_content: bool = True
    ) -> list[ScrapedArticle]:
        """Scrape crime news articles from La Nación.

        Args:
            max_articles: Maximum number of articles to return (default: 20)
            fetch_full_content: Whether to fetch full article content (default: True)

        Returns:
            List of scraped articles

        Raises:
            RuntimeError: If scraping fails
        """
        try:
            # Fetch the page
            response = self.fetcher.get(self.CRIME_SECTION_URL)

            if not response:
                raise RuntimeError("Failed to fetch page - no response received")

            # Get the HTML content
            html_content = str(response)
            if not html_content:
                raise RuntimeError("Failed to fetch page - empty content")

            # Try to find articles using CSS selectors first
            articles: list[ScrapedArticle] = []

            # Look for article elements with La Nación's structure
            article_elements = response.css("article")

            for article_elem in article_elements[:max_articles]:
                try:
                    # Extract title and URL from h3 > a
                    title_link = article_elem.css("h3.c-heading a").first
                    if not title_link:
                        continue

                    title = title_link.text.strip()
                    url = title_link.attrib.get("href", "")

                    # Make URL absolute if it's relative
                    if url.startswith("/"):
                        url = f"{self.BASE_URL}{url}"

                    # Filter: only include articles from /sucesos/ section
                    if "/sucesos/" not in url:
                        continue

                    # Extract description
                    desc_elem = article_elem.css("p.description-text").first
                    description = desc_elem.text.strip() if desc_elem else title

                    # Extract publication date
                    pub_date = datetime.now(UTC)
                    time_elem = article_elem.css("time").first
                    if time_elem and time_elem.attrib.get("datetime"):
                        datetime_str = time_elem.attrib.get("datetime", "")
                        if datetime_str:
                            try:
                                pub_date = datetime.fromisoformat(
                                    datetime_str.replace("Z", "+00:00")
                                )
                            except ValueError:
                                pass

                    # Extract article ID from URL
                    article_id = (
                        url.split("/")[-2] if "/story/" in url else url.split("/")[-1]
                    )

                    # Extract image URL
                    img_elem = article_elem.css("img.c-image").first
                    image_url = img_elem.attrib.get("src") if img_elem else None

                    article = ScrapedArticle(
                        title=title,
                        url=url,
                        description=description,
                        publication_date=pub_date,
                        article_id=article_id,
                        image_url=image_url,
                    )
                    articles.append(article)

                except (AttributeError, IndexError, KeyError):
                    continue

            if articles:
                # Fetch full content for each article if requested
                if fetch_full_content:
                    for article in articles[:max_articles]:
                        try:
                            article.full_content = self.scrape_article_content(
                                article.url
                            )
                        except RuntimeError:
                            # If we can't fetch the content, keep the article without it
                            article.full_content = None

                return articles[:max_articles]

            # Fallback: Try to extract from JSON if CSS selectors didn't work
            json_data = self._extract_json_data(response.text)

            # Look for content_elements array
            content_elements = json_data.get("content_elements", [])

            for article_data in content_elements:
                parsed = self._parse_article(article_data)
                if parsed:
                    articles.append(parsed)

                if len(articles) >= max_articles:
                    break

            # Fetch full content for each article if requested
            if fetch_full_content:
                for article in articles[:max_articles]:
                    try:
                        article.full_content = self.scrape_article_content(article.url)
                    except RuntimeError:
                        # If we can't fetch the content, keep the article without it
                        article.full_content = None

            return articles

        except Exception as e:
            raise RuntimeError(f"Failed to scrape articles: {e}") from e

    def scrape_article_content(self, article_url: str) -> str:
        """Scrape the full content of a specific article.

        Args:
            article_url: URL of the article to scrape

        Returns:
            Full article text content

        Raises:
            RuntimeError: If scraping fails
        """
        try:
            response = self.fetcher.get(article_url)

            if not response:
                raise RuntimeError(f"Failed to fetch article from {article_url}")

            # Extract article content - La Nación uses specific structure
            content_parts: list[str] = []

            # Try to get paragraphs from article body
            article_paragraphs = response.css("article .c-paragraph p")
            if article_paragraphs:
                for p in article_paragraphs:
                    text = p.text.strip()
                    if text and len(text) > 20:  # Filter out short fragments
                        content_parts.append(text)

            # If no content found, try alternative selectors
            if not content_parts:
                alt_selectors = [
                    ".story-body p",
                    '[itemprop="articleBody"] p',
                    "article p",
                ]
                for selector in alt_selectors:
                    elements = response.css(selector)
                    if elements:
                        for elem in elements:
                            text = elem.text.strip()
                            if text and len(text) > 20:
                                content_parts.append(text)
                        if content_parts:
                            break

            if content_parts:
                return "\n\n".join(content_parts)

            # Last resort: return error message
            raise RuntimeError("No article content found")

        except Exception as e:
            raise RuntimeError(f"Failed to scrape article content: {e}") from e


def get_scraper() -> LaNacionCrimeScraper:
    """Get a scraper instance.

    Returns:
        LaNacionCrimeScraper instance
    """
    return LaNacionCrimeScraper()
