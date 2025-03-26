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

-----Creacion de Jobs
USE [msdb]
GO
DECLARE @jobId BINARY(16)
EXEC  msdb.dbo.sp_add_job @job_name=N'JOBRecopilaInformacionEstadistica', 
		@enabled=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Recopila de la vista sys.dm_exec_query_stats', 
		@category_name=N'[Uncategorized (Local)]', 
		@owner_login_name=N'sa', @job_id = @jobId OUTPUT
select @jobId
GO
EXEC msdb.dbo.sp_add_jobserver @job_name=N'JOBRecopilaInformacionEstadistica', @server_name = N'MURENAPC\MURENA'
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_add_jobstep @job_name=N'JOBRecopilaInformacionEstadistica', @step_name=N'Ejecuta SP', 
		@step_id=1, 
		@cmdexec_success_code=0, 
		@on_success_action=1, 
		@on_fail_action=2, 
		@retry_attempts=0, 
		@retry_interval=0, 
		@os_run_priority=0, @subsystem=N'TSQL', 
		@command=N'exec InsertQueryStats', 
		@database_name=N'NWideWorldImporters', 
		@flags=0
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_update_job @job_name=N'JOBRecopilaInformacionEstadistica', 
		@enabled=1, 
		@start_step_id=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Recopila de la vista sys.dm_exec_query_stats', 
		@category_name=N'[Uncategorized (Local)]', 
		@owner_login_name=N'sa', 
		@notify_email_operator_name=N'', 
		@notify_page_operator_name=N''
GO
USE [msdb]
GO
DECLARE @schedule_id int
EXEC msdb.dbo.sp_add_jobschedule @job_name=N'JOBRecopilaInformacionEstadistica', @name=N'ten-second', 
		@enabled=1, 
		@freq_type=4, 
		@freq_interval=1, 
		@freq_subday_type=2, 
		@freq_subday_interval=10, 
		@freq_relative_interval=0, 
		@freq_recurrence_factor=1, 
		@active_start_date=20250226, 
		@active_end_date=99991231, 
		@active_start_time=0, 
		@active_end_time=235959, @schedule_id = @schedule_id OUTPUT
select @schedule_id
GO

USE [msdb]
GO
DECLARE @jobId BINARY(16)
EXEC  msdb.dbo.sp_add_job @job_name=N'JOBProcesaInformacionEstadistica', 
		@enabled=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Procesa la información capturada en QueryStats para insertarla en la tabla DSBase', 
		@category_name=N'Data Collector', 
		@owner_login_name=N'sa', @job_id = @jobId OUTPUT
select @jobId
GO
EXEC msdb.dbo.sp_add_jobserver @job_name=N'JOBProcesaInformacionEstadistica', @server_name = N'MURENAPC\MURENA'
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_add_jobstep @job_name=N'JOBProcesaInformacionEstadistica', @step_name=N'Ejecuta sp InsertDataSetBase', 
		@step_id=1, 
		@cmdexec_success_code=0, 
		@on_success_action=1, 
		@on_fail_action=2, 
		@retry_attempts=0, 
		@retry_interval=0, 
		@os_run_priority=0, @subsystem=N'TSQL', 
		@command=N'exec InsertDataSetBase', 
		@database_name=N'NWideWorldImporters', 
		@flags=0
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_update_job @job_name=N'JOBProcesaInformacionEstadistica', 
		@enabled=1, 
		@start_step_id=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Procesa la información capturada en QueryStats para insertarla en la tabla DSBase', 
		@category_name=N'Data Collector', 
		@owner_login_name=N'sa', 
		@notify_email_operator_name=N'', 
		@notify_page_operator_name=N''
GO
USE [msdb]
GO
DECLARE @schedule_id int
EXEC msdb.dbo.sp_add_jobschedule @job_name=N'JOBProcesaInformacionEstadistica', @name=N'ten-minutes', 
		@enabled=1, 
		@freq_type=4, 
		@freq_interval=1, 
		@freq_subday_type=4, 
		@freq_subday_interval=10, 
		@freq_relative_interval=0, 
		@freq_recurrence_factor=1, 
		@active_start_date=20250226, 
		@active_end_date=99991231, 
		@active_start_time=0, 
		@active_end_time=235959, @schedule_id = @schedule_id OUTPUT
select @schedule_id
GO

-----Creacion de Funcion que calcula la categoría
CREATE FUNCTION dbo.OBTENER_CATEGORIA( @tiempoEjecucion as bigint,
			@table_scan_flag as bit,
			@warnings_flag as bit,
			@index_suggestion_flag as bit )
			RETURNS int
BEGIN
	declare @categoria as varchar(15)
	IF @tiempoEjecucion <= 2000 
   AND @index_suggestion_flag = 0 
           AND @warnings_flag =0 
   AND @table_scan_flag=0 
		SET @categoria = 2--'OPTIMIZADO'	
	ELSE 
		SET @categoria = 1--'POR OPTIMIZAR'
	RETURN @categoria
END
GO
---Consulta SQL para obtener el conjunto de datos
SELECT idconsulta,
       creation_time,
       index_suggestions_flag,
       warnings_flag,
       table_scan_flag,
       index_scan_flag,
       last_execution_time,
       last_worker_time,
       last_logical_reads,
       last_elapsed_time,
       dbo.OBTENER_CATEGORIA(last_elapsed_time, table_scan_flag, warnings_flag,
			  index_suggestions_flag) Categoria
FROM   DSBASE
