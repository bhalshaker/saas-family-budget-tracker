from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import async_session
from routes import UsersRouter,FamiliesRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Closes database connections when the applications is down
    """
    yield
    async_session
    if async_session is not None:
        await async_session.close()
        
app=FastAPI(lifespan=lifespan,
            title="Family Buget Tracker RESTFul APIs",
            summary="**Collection for APIs to be act as a middleware between Mobile/Web front-ends and database and include most of the business logic**",
            description="""The Multi-Family Budget Tracking Application is a simple secure and collaborative financial management tool that allows multiple families to independently track their budgets, expenses, goals, and transactions. With built-in support for multi-tenancy, each family’s data is isolated and confidential.
Users can create accounts, categorize transactions, assign budgets, and track savings goals. This RestFull API system features a flexible many-to-many relationship between families and users, enabling shared access across households with role-based permissions.
Designed with a RESTful API structure, the application supports integration with web and mobile interfaces, empowering families to plan and manage their finances together — with clarity, control, and transparency.""",
            version="0.0.0",
            docs_url="/docs")
app.include_router(router=UsersRouter, tags=["User"])
app.include_router(router=FamiliesRouter, tags=["Family"])