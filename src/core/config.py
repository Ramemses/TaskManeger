from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent



class AuthJWT(BaseModel):
    private_key: str = Field("", alias="PRIVATE_KEY")
    public_key: str = Field("", alias="PUBLIC_KEY")
    algorithm: str = Field("RS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, alias="REFRESH_TOKEN_EXPIRE_DAYS")



class Settings(BaseSettings):
    # App settings
    app_name: str = "Authorisation_App"
    app_env: str = "development"
    debug: bool = True

    # Database settings
    database_url: str = Field(alias="DATABASE_URL")
    database_test_url: str = Field(alias="DATABASE_TEST_URL")

    # JWT settings
    auth_jwt: AuthJWT = AuthJWT()


    class Config:
        env_file = '.env'
        env_nested_delimiter = "__"
        case_sensitive = False


settings = Settings()