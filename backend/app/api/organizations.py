from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.organization import Organization as DBOrganization, OrganizationCreate, OrganizationResponse
from app.models.user import User as DBUser
from app.core.db import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.post("/organizations", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    db_organization = DBOrganization(**organization.model_dump())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    
    # Add the creating user as a member of the organization
    db_organization.members.append(current_user)
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)

    return db_organization

@router.get("/organizations", response_model=List[OrganizationResponse])
def get_all_organizations(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    # Only return organizations the current user is a member of
    return current_user.organizations

@router.get("/organizations/{org_id}", response_model=OrganizationResponse)
def get_organization(
    org_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == org_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=404, detail="Organization not found or user not a member")
    return organization

@router.post("/organizations/{org_id}/add_user/{user_id}", response_model=OrganizationResponse)
def add_user_to_organization(
    org_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == org_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=404, detail="Organization not found or user not a member")
    
    user_to_add = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user_to_add:
        raise HTTPException(status_code=404, detail="User to add not found")
    
    if user_to_add in organization.members:
        raise HTTPException(status_code=400, detail="User is already a member of this organization")
    
    organization.members.append(user_to_add)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

@router.delete("/organizations/{org_id}/remove_user/{user_id}", response_model=OrganizationResponse)
def remove_user_from_organization(
    org_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == org_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=404, detail="Organization not found or user not a member")
    
    # Only the creator can remove users for now
    if organization.members[0].id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can remove users from this organization")

    user_to_remove = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user_to_remove:
        raise HTTPException(status_code=404, detail="User to remove not found")
    
    if user_to_remove not in organization.members:
        raise HTTPException(status_code=400, detail="User is not a member of this organization")
    
    organization.members.remove(user_to_remove)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

@router.delete("/organizations/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    org_id: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    organization = db.query(DBOrganization).filter(DBOrganization.id == org_id).first()
    if not organization or current_user not in organization.members:
        raise HTTPException(status_code=404, detail="Organization not found or user not a member")
    
    # For simplicity, only the creator/first member can delete for now.
    # More robust permission system would be needed for production.
    if organization.members[0].id != current_user.id:
         raise HTTPException(status_code=403, detail="Only the creator can delete this organization")

    db.delete(organization)
    db.commit()
    return