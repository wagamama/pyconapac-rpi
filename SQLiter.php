<?php

class SQLiter extends SQLite3 
{
	private $_handle;
	private $_str    = '';
	private $_whereS = array();
	private $_valueS = array();
	private $_lastErrorCode = 0;
	private $_lastErrorMsg  = '';
	private $_maxRetry = 1;

	function __construct($db) 
	{
		try
		{
			$this->_handle = new SQLite3($db);
			//$this->_handle->busyTimeout(3000);
		}
		catch (Exception $e) 
		{
			throw $e;
		}
	}


	public function select() 
	{
		$argc = func_num_args();
		$argv = func_get_args();

		if (is_array($argv[0]))
		{
			$this->_str = 'SELECT ';

			foreach ($argv[0] as $field)
			{
				$this->_str .= "`$field`, ";
			}

			$this->_str = substr($this->_str, 0, strlen($this->_str)-2);
		}
		else
		{
			if ($argc >= 1) 
			{
				$str = implode(',', $argv);
				$this->_str = 'SELECT ' . $str;
			} else {
				$this->_str = 'SELECT * ';
			}
		}

		return $this;
	}

	public function from($from) 
	{
		$this->_str .= " FROM `$from`";

		return $this;
	}

	public function where() 
	{
		$argc = func_num_args();
		$argv = func_get_args();

		$this->_whereS = $argv[0];

		$condition = '';

		if (is_array($argv[0]))
		{
			foreach ($argv[0] as $fieldS => $valueS) 
			{
				if (is_array($valueS))
				{
					// bindParam
					/*
					$field   = $valueS[0];
					$operand = $valueS[1];
					$condition .= "$field $operand :$field AND ";
					 */
					// bindValue
					$field   = $valueS[0];
					$operand = $valueS[1];
					$condition .= "$field $operand ? AND ";
				}
				// default
				else
				{
					$condition .= $fieldS . '=:' . $fieldS . ' AND ';
				}
			}

			$this->_str .= ' WHERE ' . substr($condition, 0, strlen($condition)-5);
		}

		return $this;
	}

	public function orderBy()
	{
		$argc = func_num_args();
		$argv = func_get_args();

		$orderby = '';

		if ($argc == 1) 
		{
			foreach ($argv[0] as $order => $by) 
			{
				$orderby .= $order . ' ' . $by;
			}

			$this->_str .= ' ORDER BY ' . substr($orderby, 0, strlen($orderby));
		}

		return $this;
	}


	public function limit() 
	{
		$argc = func_num_args();
		$argv = func_get_args();

		$limit = '';

		if ($argc == 1) 
		{
			$limit = $argv[0];

			$this->_str .= ' LIMIT ' . $limit;
		}

		return $this;
	}


	public function get() 
	{
		$stmt = $this->_handle->prepare($this->_str);

		if ( ! is_object($stmt))
		{
			$this->_lastErrorCode = $this->_handle->lastErrorCode();
			$this->_lastErrorMsg  = $this->_handle->lastErrorMsg();

			return FALSE;
		}

		$counter = 0;

		foreach ($this->_whereS as $fieldS => $valueS) 
		{
			if (is_array($valueS))
			{
				// bindValue
				$counter++;
				$field   = $valueS[0];
				$operand = $valueS[1];
				$value   = $valueS[2];
				$type    = $valueS[3];

				switch ($type)
				{
				case SQLITE3_INTEGER:
					$stmt->bindParam($counter, intval($value),   $type);
					break;
				case SQLITE3_FLOAT:
					$stmt->bindParam($counter, floatval($value), $type);
					break;
				case SQLITE3_TEXT:
					$stmt->bindParam($counter, $value, $type);
					break;
				case SQLITE3_BLOB:
					$stmt->bindParam($counter, $value, $type);
					break;
				case SQLITE3_NULL:
					$stmt->bindParam($counter, $value, $type);
					break;
				default:
					$stmt->bindParam($counter, $value, $type);
					break;
				}

			}
			// default
			else
			{
				$stmt->bindParam(":$fieldS", $valueS);
			}
		}

		$retry = 0;

		do {
			if ($retry !== 0) ;
			$retry++;

			$result = $stmt->execute();

			if ($retry > $this->_maxRetry)
			{
				break;
			}
		}
		while ($result == FALSE);

		if ($result == FALSE)
		{
			$this->_lastErrorCode = $this->_handle->lastErrorCode();
			$this->_lastErrorMsg  = $this->_handle->lastErrorMsg();

			return FALSE;
		}

		$resultArray = array();
		while ($resultArray[] = $result->fetchArray(SQLITE3_ASSOC)) {}
		array_pop($resultArray);

		$result->finalize();
		$stmt->clear();
		$stmt->close();
		$this->_valueS = array();
		$this->_whereS = array();
		$this->_str = '';

		return $resultArray;
	}

	public function insert() 
	{
		$argc = func_num_args();
		$argv = func_get_args();
		$this->_valueS = $argv[0];
		$field_str = '';
		$value_str = '';

		if (is_array($argv[0]))
		{
			foreach ($argv[0] as $field => $value) 
			{
				$field_str .= "`$field`,";	
				$value_str .= ":$field,";
			}

			$field_str = substr($field_str, 0, strlen($field_str)-1);
			$value_str = substr($value_str, 0, strlen($value_str)-1);
			$this->_str = "($field_str) VALUES ($value_str)";
		}

		return $this;
	}

	public function into($into) 
	{
		$this->_str = "INSERT INTO `$into` $this->_str";

		return $this;
	}

	public function update() 
	{
		$argc = func_num_args();
		$argv = func_get_args();

		$this->_valueS = $argv[0];

		if (is_array($argv[0]))
		{
			foreach ($argv[0] as $field => $value) 
			{
				$this->_str .= "`$field`=:$field,";
			}

			$this->_str = substr($this->_str, 0, strlen($this->_str)-1);
		}

		return $this;
	}

	public function set($set) 
	{
		$this->_str = "UPDATE `$set` SET $this->_str";

		return $this;
	}


	public function delete() 
	{
		$this->_str = 'DELETE ';

		return $this;
	}


	public function execute() 
	{
        //print_r($this->_str);

		$stmt = $this->_handle->prepare($this->_str);

		if ( ! is_object($stmt))
		{
			return FALSE;
		}


		if ( ! empty($this->_valueS))
		{
			foreach ($this->_valueS as $field => $value) 
			{
				$stmt->bindParam(":$field", $this->_valueS[$field]);
			}
		}
		if ( ! empty($this->_whereS))
		{
			$counter = 0;

			foreach ($this->_whereS as $fieldS => $valueS) 
			{
				if (is_array($valueS))
				{
					// bindParam
					/*
					$field   = $valueS[0];
					$operand = $valueS[1];
					$value   = $valueS[2];
					$type    = $valueS[3];

					switch ($type)
					{
					case SQLITE3_INTEGER:
						$stmt->bindParam(":$field", intval($value),   $type);
						break;
					case SQLITE3_FLOAT:
						$stmt->bindParam(":$field", floatval($value), $type);
						break;
					case SQLITE3_TEXT:
						$stmt->bindParam(":$field", $value, $type);
						break;
					case SQLITE3_BLOB:
						$stmt->bindParam(":$field", $value, $type);
						break;
					case SQLITE3_NULL:
						$stmt->bindParam(":$field", $value, $type);
						break;
					default:
						$stmt->bindParam(":$field", $value, $type);
						break;
					}
					 */

					// bindValue
					$counter++;
					$field   = $valueS[0];
					$operand = $valueS[1];
					$value   = $valueS[2];
					$type    = $valueS[3];

					switch ($type)
					{
					case SQLITE3_INTEGER:
						$stmt->bindParam($counter, intval($value),   $type);
						break;
					case SQLITE3_FLOAT:
						$stmt->bindParam($counter, floatval($value), $type);
						break;
					case SQLITE3_TEXT:
						$stmt->bindParam($counter, $value, $type);
						break;
					case SQLITE3_BLOB:
						$stmt->bindParam($counter, $value, $type);
						break;
					case SQLITE3_NULL:
						$stmt->bindParam($counter, $value, $type);
						break;
					default:
						$stmt->bindParam($counter, $value, $type);
						break;
					}

				}
				// default
				{
					$stmt->bindParam(":$fieldS", $valueS);
				}
			}
		}


		$retry = 0;
		do {
			if ($retry !== 0) ;

			$retry++;

			$result = $stmt->execute();

			//if ($result == FALSE)	usleep( rand(1, 3)*100000 );

			if ($retry > $this->_maxRetry)
			{
				break;
			}
		}
		while ($result == FALSE);


		$this->_valueS = array();
		$this->_whereS = array();
		$this->_str = '';

		if ($result == FALSE)
		{
			$this->_lastErrorCode = $this->_handle->lastErrorCode();
			$this->_lastErrorMsg  = $this->_handle->lastErrorMsg();

			$stmt->clear();
			$stmt->close();

			return FALSE;
		}
		else
		{
			$result->finalize();
			$stmt->clear();
			$stmt->close();

			return TRUE;
		}
	}

	public function truncate()
	{
		$this->_str = 'DELETE ';

		return $this;
	}


	public function direct_query($str) 
	{
		$str = 'BEGIN; ' . $str . ' COMMIT;';

		$retry = 0;

		do {
			if ($retry !== 0) ;

			$retry++;

			$result = $this->_handle->exec($str);

			//if ($result == FALSE)	usleep( rand(1, 3)*100000 );

			if ($retry > $this->_maxRetry)
			{
				break;
			}
		}
		while ($result == FALSE);

		return $result;
	}

	public function echoTest($var)
	{
	}

	function getError()
	{
		return $this->_lastErrorMsg;
	}

	function __destruct() 
	{
		$this->_str  = '';
		$this->_whereS = array();
		$this->_valueS = array();
		$this->_handle->close();
	}

}

