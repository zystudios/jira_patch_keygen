<?php
/**
 * Patch Script for Atlassian JIRA
 *
 * @author sskaje (http://sskaje.me/)
 */

echo <<<COPYRIGHT
Patch Script for Atlassian JIRA

Author: sskaje (http://sskaje.me/)

COPYRIGHT;

if (!isset($argv[1]) || !is_dir($argv[1])) {
    usage();
}
/**
 * New key
 */
$new_key = "MIIBtjCCASsGByqGSM44BAEwggEeAoGBAKLDYyvaCCrsJ1b9HBlQJXeYjR6ztdiRsmIokZliQow0EN4OshlJxLISa1ME255pqgBoRMjmX8mp5naFT/OjGH4AQMGrBazoStPTXND7unHCeE9TMHzOWtWL5sm1rNr0C5lOOLFdIJg6xFooheXMT+SVYXoVvfBDAglv8hPmq9qvAhUAi2f/089USnWQO0t5LzRUrkA8V/cCgYBIxQSytAVW9r/Y/CKqDuIpZWZRsFWG6L7CE4uCDdyVKHYg49kY8rhVw0NQMbeBlLKAsYXgYmdCqPUDLrNJLoV5doEQwSkOclkKgQYWWbr53gdG/8EjyzGqQcVpDqm7hwVkbwRYJbyTEkUCmmN8ZKnFnpeh2hbJwoDec9ReyPlKvgOBhAACgYBK/dX85LEVJKhg2wjqOyjkFgQGTtCidCyXnhV4FvikWfOvSthdZ5w7xIYCtqXS3dhmIvsdprAAu4uVjZwpAG2rG6TcOHhZrUFTGin0adnN21GqCWqiXhQeIEW7iaKts1quC/8djpjLcQke0OIRFK0YoI+55Kj/SBD4ensd9Z//+g==";
/**
 * Old key hard-coded in Version2LicenseDecoder.class
 */
$old_key = "MIIBuDCCASwGByqGSM44BAEwggEfAoGBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAhUAl2BQjxUjC8yykrmCouuEC/BYHPUCgYEA9+GghdabPd7LvKtcNrhXuXmUr7v6OuqC+VdMCz0HgmdRWVeOutRZT+ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN/C/ohNWLx+2J6ASQ7zKTxvqhRkImog9/hWuWfBpKLZl6Ae1UlZAFMO/7PSSoDgYUAAoGBAIvfweZvmGo5otwawI3no7Udanxal3hX2haw962KL/nHQrnC4FG2PvUFf34OecSK1KtHDPQoSQ+DHrfdf6vKUJphw0Kn3gXm4LS8VK/LrY7on/wh2iUobS2XlhuIqEc5mLAUu9Hd+1qxsQkQ50d0lzKrnDqPsM0WA9htkdJJw2nS";

$path = realpath($argv[1]);
if (!$path) {
    error("Invalid path");
}

$files = find_jars($path);

if (empty($files)) {
    error("No Version2LicenseDecoder found!");
}

# Patch all jars found
foreach ($files as $file) {
    patch($file);
}
/**
 * Patch file
 *
 * @param string $file
 */
function patch($file, $_level=0) {
    pmsg("Processing file '{$file}'\n", $_level);
    
    # is writable?
    if (!is_writable($file) || !is_writable(dirname($file))) {
        error("File not writable!");
    }

    if ($_level == 0) {
        # Backup only if it's jars from
        $backup_file = $file . '.bak' . microtime(1);
        if (!copy($file, $backup_file)) {
            error("Failed to backup!");
        }
    }
    
    # Temporary Folder
    $temp_dir = '/tmp/jira-patch-' . uniqid('', true);
    if (!mkdir($temp_dir)) {
        error("Failed to create {$temp_dir}");
    }

    # Extract files
    $command = "unzip -d '{$temp_dir}' '{$file}' 2>&1 1>/dev/null ";
    system($command);
    pmsg("Files extracted to {$temp_dir}\n", $_level);

    # counter
    $count_patched_files = 0;

    # Find class file
    $class_files = find_classes($temp_dir);

    global $old_key, $new_key;

    # Patch & replace
    foreach ($class_files as $f) {
        # Read file & replace
        $content = file_get_contents($f);
        $count = 0;
        $content = str_replace($old_key, $new_key, $content, $count);
        # Check if file is patched
        if (!$count) {
            pmsg("It seems '{$f}' has already been patched.\n", $_level);
            continue;
        }
            # Save patched content
        file_put_contents($f, $content);

        ++$count_patched_files;
    }

    $jar_files = find_jars($temp_dir);
    
    foreach ($jar_files as $f) {
        $count_patched_files += patch($f, $_level+1);
    }

    if ($count_patched_files) {
        # jar -uf
        $command = "cd '{$temp_dir}'; zip -u {$file}";
        system($command);
        pmsg("{$file} updated\n", $_level); 
    } else if (isset($backup_file)) {
        pmsg("Cancelling backup files\n", $_level);
        unlink($backup_file);
    }

    # Clean up
    pmsg("Removing {$temp_dir}\n", $_level);
    system("rm -fr '{$temp_dir}'");

    pmsg("{$count_patched_files} class file(s) in {$file} processed\n\n", $_level);

    return $count_patched_files;
}

function pmsg($msg, $_level) {
    if ($_level) {
        echo str_repeat("\t", $_level);
    }
    echo $msg;
}


function execute_command($command)
{
    $result = array();
                                                               
    $h = popen($command, 'r');                             
    while (!feof($h)) {                                    
        $l = trim(fgets($h));                          
        if ($l) {                                      
            $result[] = $l;                         
        }                                              
    }                                                      
    pclose($h);                                            
     
    return $result;                                                              
}

function find_jars($path) {
    $command = "find '{$path}' -name '*.jar' -exec grep -l Version2LicenseDecoder {} \\;";
    $files = execute_command($command);
    return $files;
}


function find_classes($path) {
    $command = "find '{$path}' -name Version2LicenseDecoder.class";  
    $files = execute_command($command);
    return $files;
}



/**
 * Usage
 */
function usage() {
        global $argv, $argc;
        echo <<<USAGE
{$argv[0]} PATH_TO_JIRA

USAGE;
        exit;
}

/**
 * Print error and exit
 *
 * @param string $msg
 */
function error($msg) {
    echo "Error: " . trim($msg) . "\n";
    exit; 
}

# EOF
