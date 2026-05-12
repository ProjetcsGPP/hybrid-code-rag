# pipeline/structure/resolver/call_matcher.py


class CallMatcher:

    def match(self, call_name: str, context):

        candidates = []

        # 1. match direto por nome
        candidates += context.index.by_name.get(call_name, [])

        # 2. mesmo módulo
        candidates += context.index.by_module.get(context.module, [])

        # 3. mesmo escopo de classe
        if context.class_name:
            candidates += context.index.by_class.get(context.class_name, [])

        return candidates