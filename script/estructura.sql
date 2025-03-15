---Creacion de tablas
CREATE TABLE QueryStats (
	query_id bigint identity primary key,
    sql_handle varbinary(64),
    plan_handle varbinary(64),
	query varchar(max),
	query_plan xml,
    execution_count bigint,
    total_worker_time bigint,
    total_physical_reads bigint,
    total_logical_reads bigint,
    total_logical_writes bigint,
    total_elapsed_time bigint,
    creation_time datetime,
    last_execution_time datetime,
		last_worker_time bigint,
		last_logical_reads bigint,
		last_elapsed_time bigint
);

CREATE TABLE DSBase(
	IDConsulta INT Identity,
	Creation_Time DATETIME NOT NULL,
	Query varchar(MAX)  not null,
	Index_Suggestions_Flag bit not null default 0,
	Warnings_Flag bit not null default 0,
	Table_Scan_Flag bit not null default 0,
	Index_Scan_Flag bit not null default 0,
    last_execution_time DATETIME NOT NULL,
	last_worker_time bigint not null,
	last_logical_reads bigint not null,
	last_elapsed_time bigint not null
);
GO;
-----Procedimientos almacenados

CREATE PROCEDURE InsertQueryStats
AS
BEGIN
    INSERT INTO QueryStats
   SELECT 
        sql_handle,
	    sys.dm_exec_query_stats.plan_handle,
		dm_exec_sql_text.text,
		dm_exec_query_plan.query_plan,
        execution_count,
        total_worker_time,
        total_physical_reads,
        total_logical_reads,
        total_logical_writes,
        total_elapsed_time,
        creation_time,
        last_execution_time,
		last_worker_time,
		last_logical_reads,
		last_elapsed_time
    FROM sys.dm_exec_query_stats 
		CROSS APPLY sys.dm_exec_sql_text(dm_exec_query_stats.plan_handle)
		CROSS APPLY sys.dm_exec_query_plan(dm_exec_query_stats.plan_handle)
		INNER JOIN sys.databases 	ON dm_exec_sql_text.dbid = databases.database_id
		INNER JOIN sys.dm_exec_cached_plans 	ON dm_exec_cached_plans.plan_handle = dm_exec_query_stats.plan_handle
	WHERE databases.name = 'NWideWorldImporters' --Nombre de la base de datos
		AND  dm_exec_cached_plans.objtype = 'Adhoc'
		--AND last_execution_time > (CASE WHEN (SELECT max(last_execution_time) FROM QueryStats qs where qs.sql_handle = sql_handle and qs.plan_handle = sys.dm_exec_query_stats.plan_handle) IS NOT NULL THEN (SELECT max(last_execution_time) FROM QueryStats qs where qs.sql_handle = sql_handle and qs.plan_handle = sys.dm_exec_query_stats.plan_handle) ELSE (SELECT DATEADD(Minute,-5, GETDATE())) END )
		AND last_execution_time > (CASE WHEN (SELECT max(qs.last_execution_time) FROM QueryStats qs ) IS NOT NULL THEN (SELECT max(qs.last_execution_time) FROM QueryStats qs) ELSE (SELECT DATEADD(Minute,-5, GETDATE())) END )
	  and CHARINDEX('sys.dm_exec_query_stats', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('QueryStats', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('DSBase', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.dm_os_host_info', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.dm_exec_connections', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.sys.schemas', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.triggers', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.sql_modules', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.certificates', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.database_principals', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('sys.assembly_types', dm_exec_sql_text.text) = 0 AND  
	  CHARINDEX('SCHEMA_NAME', dm_exec_sql_text.text) = 0;
END;
GO;

CREATE PROCEDURE InsertDataSetBase
AS
BEGIN
	insert into DSBase (Query, Creation_Time, Index_Suggestions_Flag,Warnings_Flag,Table_Scan_Flag,Index_Scan_Flag,last_execution_time,last_worker_time,last_logical_reads,last_elapsed_time)
	select query, creation_time
		,case when CAST(qs.query_plan as nvarchar(max)) LIKE '%<MissingIndex%' then 1 else 0 end
		,case when CAST(qs.query_plan as nvarchar(max)) LIKE '%<Warnings>%' then 1 else 0  end
		,case when CAST(qs.query_plan as nvarchar(max)) LIKE '%<TableScan%' then 1 else 0 end
		,case when CAST(qs.query_plan as nvarchar(max)) LIKE '%<IndexScan%' then 1 else 0 end
		,last_execution_time,
		last_worker_time,
		last_logical_reads,
		last_elapsed_time
	from dbo.QueryStats qs
	where last_execution_time  > (CASE WHEN (SELECT max(last_execution_time) FROM DSBase) IS NOT NULL THEN (SELECT max(last_execution_time) FROM DSBase) ELSE (SELECT DATEADD(Minute,-5, GETDATE())) END )
END;

