from mtmai.agents.chat_profiles.chat_post_gen import PostGenAgent
from mtmai.agents.chat_profiles.site_settings_agent import SiteSettingsAgent

all_chat_agents = [PostGenAgent, SiteSettingsAgent]


async def get_all_profiles():
    all_profiles = [agent.get_chat_profile() for agent in all_chat_agents]
    return all_profiles


async def get_default_chat_profile():
    return next(
        (profile for profile in await get_all_profiles() if profile.default), None
    )
