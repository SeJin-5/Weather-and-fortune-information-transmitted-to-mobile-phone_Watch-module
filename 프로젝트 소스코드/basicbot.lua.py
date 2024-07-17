auth_phone  = { ["821042540545"] = true, 
                ["821087109936"] = true, }



our_id = 0


function vardump(value, depth, key)
    local linePrefix = ""
    local spaces = ""

    if key ~= nil then
    linePrefix = "["..key.."] = "
    end

    if depth == nil then
    depth = 0
    else
    depth = depth + 1
    for i=1, depth do spaces = spaces .. "  " end
    end

    if type(value) == 'table' then
        mTable = getmetatable(value)
    if mTable == nil then
        print(spaces ..linePrefix.."(table) ")
    else
        print(spaces .."(metatable) ")
        value = mTable
    end
    for tableKey, tableValue in pairs(value) do
        vardump(tableValue, depth, tableKey)
    end
    elseif type(value) == 'function' or 
        type(value) == 'thread' or 
        type(value) == 'userdata' or
        value == nil
    then
        print(spaces..tostring(value))
    else
        print(spaces..linePrefix.."("..type(value)..") "..tostring(value))
    end
end


function Hello(user_id)
    send_msg(user_id, '"https://fortune.nate.com/contents/freeunse/freeunseframe.nate?freeUnseId=today03" 오늘의 운세입니다', ok_cb, false)
end

function GetWether(user_id, arg)
    send_msg(user_id, '"https://www.weather.go.kr/w/index.do" 오늘의 날씨입니다', ok_cb, false)
end


function SendHelp(user_id)
    send_text(user_id, '/home/pi/tg/bot/help.txt', ok_cb, false)
end


function msg_processing(user_id, cmd, arg)
    if     ( cmd == '운세' )        then    Hello(user_id)
    elseif ( cmd == '날씨' )        then    GetWether(user_id, arg)
    elseif ( cmd == 'help' )    then    SendHelp(user_id)
    end
end

function on_msg_receive (msg)
    vardump(msg)

    if msg.out then
        print("-- : ", msg.out, "\n")
        return
    end

    if auth_phone[msg.from.phone] then
        print "auth    : OK "
    else
        print "auth    : invalid user"
        return
    end

    local cmd, arg  = split(msg.text)

    cmd = string.lower(cmd)
    print("receive  : [", cmd, "]\n")
    print("argument : [", arg, "]\n")

    print("Name     : ", msg.from.print_name)
    print("Phone    : ", msg.from.phone)
    print("Msg Num  : ", msg.id)
    print("to.Name  : ", msg.to.print_name)

    if (msg.to.id == our_id) then
        user_id = msg.from.print_name
    else
        user_id = msg.to.print_name
    end

    mark_read(user_id, ok_cb, false)

    msg_processing(user_id, cmd, arg)

end

function on_secret_chat_created (peer)
    print "secret chat create event"
end

function on_secret_chat_update (schat, what)
    print "secret chat update event"
end

function on_user_update (user)
    print "user update event"
end

function on_chat_update (user)
    print "chat update event"
end
 
function on_our_id(id)
    our_id = id
    print("My user# : ", id)
end

function on_get_difference_end ()
end

function on_binlog_replay_end ()
end

function ok_cb(extra, success, result)
end


function trim(s)
  return (s:gsub("^%s*(.-)%s*$", "%1"))
end


function split(str)
    local cmd=""
    local arg=""
    local arg_cnt=1

    for s in string.gmatch(str, "[^%s]+") do
        if ( arg_cnt == 1 ) then
            cmd = s
        else
            arg = arg .." ".. s
        end
        arg_cnt = arg_cnt + 1
    end

    cmd = trim(cmd)
    arg = trim(arg)

    return cmd, arg
end
