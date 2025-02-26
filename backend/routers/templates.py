from fastapi import APIRouter, HTTPException
from typing import List
from backend.models.schemas import SQLTemplate, SQLTemplateCreate, SQLTemplateUpdate
from backend.database.mysql import get_system_db_connection
from backend.journal.logging import logger

router = APIRouter(prefix="/api/templates")

@router.get("/", response_model=List[SQLTemplate])
async def get_templates():
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sql_templates")
        templates = cursor.fetchall()
        cursor.close()
        conn.close()
        return templates
    except Exception as e:
        logger.error(f"获取模板列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取模板列表失败")

@router.post("/", response_model=SQLTemplate)
async def create_template(template: SQLTemplateCreate):
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO sql_templates (description, sql_text, scenario) VALUES (%s, %s, %s)",
            (template.description, template.sql_text, template.scenario)
        )
        template_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return SQLTemplate(id=template_id, **template.dict())
    except Exception as e:
        logger.error(f"创建模板失败: {e}")
        raise HTTPException(status_code=500, detail="创建模板失败")

@router.put("/{template_id}", response_model=SQLTemplate)
async def update_template(template_id: int, template: SQLTemplateUpdate):
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        update_fields = {k: v for k, v in template.dict().items() if v is not None}
        if not update_fields:
            raise HTTPException(status_code=400, detail="没有提供更新字段")
            
        query = "UPDATE sql_templates SET " + ", ".join(f"{k} = %s" for k in update_fields.keys())
        query += " WHERE id = %s"
        
        cursor.execute(query, (*update_fields.values(), template_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="模板不存在")
            
        cursor.close()
        conn.close()
        
        return SQLTemplate(id=template_id, **update_fields)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新模板失败: {e}")
        raise HTTPException(status_code=500, detail="更新模板失败")

@router.delete("/{template_id}")
async def delete_template(template_id: int):
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sql_templates WHERE id = %s", (template_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="模板不存在")
            
        cursor.close()
        conn.close()
        return {"message": "模板删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除模板失败: {e}")
        raise HTTPException(status_code=500, detail="删除模板失败") 